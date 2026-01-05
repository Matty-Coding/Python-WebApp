from json import loads, dump
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from re import match

import logging

from typing import Any

# =========================

# Definizione cartella dati
DATA_PATH = Path("scripting/data")
DATA_PATH.mkdir(exist_ok=True)

# Definizione cartella di log
LOG_DIR = Path("scripting/logs")
LOG_DIR.mkdir(exist_ok=True)


# =========================
# ======  LOGGER  =========
# =========================


def get_logger(name: str) -> logging.Logger:
    """
    Restituisce un oggetto `Logger` con il nome specificato.
    """

    # Definizione nome logger dinamico
    logger = logging.getLogger(name)

    # Settaggio livello logger
    logger.setLevel(logging.DEBUG)

    # Controllo presenza handler + creazione
    if not logger.handlers:

        # Definizione nome file di log
        log_file = LOG_DIR / f"{name}.log"

        # Definizione handler per il file (log di tutto, sovrascritto ogni volta)
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Definizione handler per la console (solo errori e superiori)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Definizione formattazzione dei logger
        formatter = logging.Formatter(
            "%(asctime)s | %(module)s | %(funcName)s [%(levelname)s]: %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )

        # Configurazione formattazione handler
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Aggiunta degli handler al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Restituzione oggetto logger
    return logger


# ============================================
# ===========  GENERATE API CLASS  ===========
# ============================================


class LeagueAPI:
    """
    Gestisce le richieste alle API statiche di League of Legends (Data Dragon).

    Usa una sessione HTTP per ottimizzare le connessioni e fornisce un metodo interno `_get`
    per fare richieste sicure e centralizzare la gestione degli errori.
    """

    # Costruttore classe
    def __init__(self, base_url="https://ddragon.leagueoflegends.com/"):
        self._base_url = base_url

        # Inizializzazione sessione
        self.session = requests.Session()

        # Inizializzazione logger
        self._extracting_log = "extracting_data"
        self._logger = get_logger(self._extracting_log)

        # Inizializzazione dizionario (caching dati)
        self._champions_data: dict[str, dict] = {}

    def _get(self, url: str) -> dict[str, Any]:
        """
        Esegue una `GET` usando la sessione.
        Gestisce gli errori delle richieste e restituisce `JSON`.
        """

        # Blocco try/except per la gestione degli errori
        try:

            # Tentativo di richiesta HTTP
            response = self.session.get(url)
            response.raise_for_status()
            self._logger.info(f"ℹ️ Connessione a: {url}")

            # Restituzione `JSON` della risposta
            return response.json()

        # Cattura errore timeout
        except requests.Timeout:
            self._logger.error(f"⚠️ Timeout nella richiesta verso: {url}")
            raise

        # Cattura errori generali
        except requests.RequestException as e:
            self._logger.error(f"⚠️ Errore nella richiesta verso: {url}: {e}")
            raise

    def get_versions(self, last_version: bool = False) -> tuple[str]:
        """
        Restituisce una tupla di stringhe relative a tutte le patch.

        Se `last_version` viene impostato come `True` restituisce solo l'ultima versione.
        """

        url = f"{self._base_url}/api/versions.json"
        data = self._get(url)

        self._logger.info(f"✔️ Versioni scaricate.")
        return data[0] if last_version else tuple(data)

    # Metodo per ottenere le lingue con codici, stati e lingua (scraping statico)
    def get_languages(
        self, country: str = None
    ) -> tuple[dict[str, str]] | dict[str, str]:
        """
        Restituisce una tupla di dizionari contenenti informazioni riguardo le lingue.

        Se `country` viene specificato ed è presente nella tupla, restituisce solo il relativo dizionario.
        """

        try:
            url = "https://developer.riotgames.com/docs/lol#data-dragon_languages"
            response = requests.get(url)
            response.raise_for_status()

            self._logger.info(f" ℹ️Connessione a: {url}")

            soup = BeautifulSoup(response.text, "html.parser")
            tables = soup.select("table")

            # Ricerca tabella con header "code" e "language"
            for table in tables:
                headers = [th.get_text(strip=True).lower() for th in table.select("th")]

                if "code" in headers and "language" in headers:
                    rows = [tr.get_text(strip=True) for tr in table.select("tr")][1:]
                    pattern = r"^(?P<code>[a-z_A-Z]{5})(?P<lang>[a-zA-Z]+) \((?P<country>[a-z A-Z]+)\)$"

                    # Estrazione informazioni (esclusione dati non aggiornati)
                    language_info = tuple(
                        [
                            match(pattern, row).groupdict()
                            for row in rows
                            if "ms_MY" not in row
                        ]
                    )

            self._logger.info(f"✔️ Informazioni sulle lingue scaricate.")

            # Opzione per restituire informazioni di una singola lingua
            if country and isinstance(country, str):
                for element in language_info:
                    if country.lower() == element["country"].lower():
                        return element
            else:
                return language_info

        except requests.Timeout:
            self._logger.error(f"⚠️ Timeout nella richiesta verso: {url}")
            raise

        except requests.RequestException as e:
            self._logger.error(f"⚠️ Errore nella richiesta verso: {url}: {e}")
            raise

    def get_champions(self, patch: str, code_lang: str) -> tuple[tuple[str, dict]]:
        """
        Restituisce una tupla di tuple contenenti come primo elemento l'id del campione e come secondo i dizionari aventi `name` e `nickname`
        """

        url = f"{self._base_url}cdn/{patch}/data/{code_lang}/champion.json"
        data = self._get(url)

        self._logger.info(f"✅ Informazioni sui nomi dei campioni scaricate.")

        return tuple(
            [
                (info["id"], {"name": info["name"], "nickname": info["title"]})
                for info in data["data"].values()
            ]
        )

    def get_abilities(self, patch: str, code_lang: str) -> tuple[tuple[str, dict]]:
        """
        Restituisce una tupla contenente id del campione e un dizionario con le sue abilità.
        """

        champion_ids = [id[0] for id in self.get_champions(patch, code_lang)]

        self._logger.info(f"ℹ️ Scaricando le abilità...")

        champ_abilities = []
        for champ_id in champion_ids:
            url = (
                f"{self._base_url}cdn/{patch}/data/{code_lang}/champion/{champ_id}.json"
            )
            data = self._get(url)
            self._champions_data[champ_id] = data["data"][champ_id]

            abilities_dict = {
                "passive": {
                    "name": data["data"][champ_id]["passive"]["name"],
                    "description": BeautifulSoup(
                        data["data"][champ_id]["passive"]["description"], "html.parser"
                    ).get_text(),
                }
            }

            ability_keys = ("q", "w", "e", "r")
            for spell, key in zip(data["data"][champ_id]["spells"], ability_keys):
                abilities_dict[key] = {
                    "name": spell["name"],
                    "description": BeautifulSoup(
                        spell["description"], "html.parser"
                    ).get_text(),
                }

            self._logger.info(f"✔️ Informazioni sulle abilità di {champ_id} scaricate.")
            champ_abilities.append((champ_id, abilities_dict))

        self._logger.info(f"✅ Abilità scaricate.")
        return tuple(champ_abilities)

    def get_icons(self, patch: str) -> tuple[tuple[str, dict]]:
        """
        Restituisce una tupla contenente id del campione e un dizionario con le sue icone (abilità incluse).
        """

        if not self._champions_data:
            self._logger.warning(
                "⚠️ Scaricare le informazioni sui campioni prima di scaricare le icone."
            )
            raise RuntimeError(
                "Scaricare le informazioni sui campioni prima di scaricare le icone."
            )

        self._logger.info(f"ℹ️ Scaricando le icone...")
        champ_icons = []
        for champ_id, champ_data in self._champions_data.items():
            icon_champ_id = champ_data["image"]["full"]
            icon_passive_id = champ_data["passive"]["image"]["full"]
            icon_spell_ids = [
                spell_id["image"]["full"] for spell_id in champ_data["spells"]
            ]

            icon_champ_url = f"{self._base_url}cdn/{patch}/img/champion/{icon_champ_id}"
            icon_passive_url = (
                f"{self._base_url}cdn/{patch}/img/passive/{icon_passive_id}"
            )
            icon_spell_ids_url = [
                f"{self._base_url}cdn/{patch}/img/spell/{spell_id}"
                for spell_id in icon_spell_ids
            ]

            icons_dict = {
                "champ_icon": icon_champ_url,
                "passive_icon": icon_passive_url,
            }

            abilities = ("q", "w", "e", "r")
            for spell_url, ability in zip(icon_spell_ids_url, abilities):
                icons_dict[f"{ability}_icon"] = spell_url

            self._logger.info(f"✔️ Informazioni sulle icone di {champ_id} scaricate.")
            champ_icons.append((champ_id, icons_dict))

        self._logger.info(f"✅ Icone scaricate .")
        return tuple(champ_icons)

    def get_skins(self) -> tuple[tuple[str, dict]]:
        """
        Restituisce una tupla contenente id del campione e un dizionario avente degli indici come chiavi e come valori `name`, `splash` e `loading.`
        """

        if not self._champions_data:
            self._logger.warning(
                "⚠️ Scaricare le informazioni sui campioni prima di scaricare le skins."
            )
            raise RuntimeError(
                "Scaricare le informazioni sui campioni prima di scaricare le skins."
            )

        self._logger.info(f"ℹ️ Scaricando le skin...")
        champ_skins = []
        for champ_id, champ_data in self._champions_data.items():

            skin_ids = [{skin["num"]: skin["name"]} for skin in champ_data["skins"]]

            skins_dict = {}
            for index, skin in enumerate(skin_ids):
                for skin_id, skin_name in skin.items():
                    if champ_id.lower() == "fiddlesticks":
                        splash_url = f"{self._base_url}cdn/img/champion/splash/FiddleSticks_{skin_id}.jpg"
                        loading_url = splash_url.replace("splash", "loading")
                    else:
                        splash_url = f"{self._base_url}cdn/img/champion/splash/{champ_id}_{skin_id}.jpg"
                        loading_url = splash_url.replace("splash", "loading")

                    skins_dict[str(index)] = {
                        "name": skin_name,
                        "splash": splash_url,
                        "loading": loading_url,
                    }

            self._logger.info(f"✔️ Informazioni sulle skin di {champ_id} scaricate.")
            champ_skins.append((champ_id, skins_dict))

        self._logger.info(f"✅ Skin scaricate.")
        return tuple(champ_skins)


# ============================================
# ===========  INHERIT API CLASS  ============
# ============================================


class Extract(LeagueAPI):
    def __init__(self):
        super().__init__()
        self._patch = self.get_versions(last_version=True)
        self._DATA_PATH = DATA_PATH

    # Metodo per scaricare le lingue, singola volta e solo se non esiste già un file

    def languages_to_json(self) -> str:
        """
        Scarica le lingue tramite il metodo contenuto in LeagueAPI e le inserisce all'interno di un `JSON` formattato.

        Restituisce il path in cui è stato creato o è già presente il file.
        """

        filename = "languages.json"
        json_lang_path = self._DATA_PATH / filename
        json_lang_path.parent.mkdir(exist_ok=True)

        if not json_lang_path.exists():
            languages = self.get_languages()

            json_dict = {}

            for lang in languages:
                json_dict[lang.get("country").lower()] = {
                    "code": lang.get("code"),
                    "language": lang.get("lang"),
                    "country": lang.get("country"),
                }

            self._logger.info("ℹ️ Creazione JSON delle lingue in corso...")
            with open(json_lang_path, "w+", encoding="utf-8") as file:
                dump(json_dict, file, indent=4)

            self._logger.info(f"ℹ️ JSON path: {json_lang_path}")
            self._logger.info(f"✅ JSON delle lingue creato.")

        else:
            self._logger.info(f"ℹ️ JSON delle lingue già esistente in {json_lang_path}.")

        return json_lang_path

    def data_champs_to_json(self, countries: tuple[str]) -> None:
        """
        Estrazione dati dei campioni ed esportazione in un file `JSON`
        """

        self._logger.info("ℹ️ Caricamento JSON di informazioni sulle lingue in corso...")
        with open(self.languages_to_json(), "r", encoding="utf-8") as json_lang:
            lang_data = loads(json_lang.read())

        self._logger.info("✅ Caricamento completato.")

        champ_dict = {}

        json_champ_folder = self._DATA_PATH / "champ"
        json_champ_folder.mkdir(exist_ok=True)

        for lang in countries:
            lang_name = lang_data[lang].get("language").lower()
            country = lang_data[lang].get("country").replace(" ", "_").lower()
            filename = f"{country}_data.json"

            json_champ_path = json_champ_folder / filename

            code = lang_data[lang].get("code")

            self._logger.info(f"ℹ️ Scaricando informazioni... ({lang_name})")

            champions = self.get_champions(patch=self._patch, code_lang=code)
            # tupla con solo id dei campioni
            champ_ids = tuple([element[0] for element in champions])
            # tupla con dict dei nomi, chiavi -> (name, nickname)
            champ_name_nickname = tuple([element[1] for element in champions])

            abilities = self.get_abilities(patch=self._patch, code_lang=code)
            # tupla con dict delle abilità, chiavi -> (passive, q, w, e, r)
            # ogni chiave ha sottochiavi -> (name, description)
            champ_abilities = tuple([element[1] for element in abilities])

            icons = self.get_icons(patch=self._patch)
            # tupla con dict delle icone
            # chiavi -> (champ_icon, passive_icon, q_icon, w_icon, e_icon, r_icon)
            champ_icons = tuple([element[1] for element in icons])

            skins = self.get_skins()
            # tupla con tuple di dict delle skins
            # chiavi di ogni dict -> (name, splash, loading)
            champ_skins = tuple([tuple(element[1].values()) for element in skins])

            self._logger.info(f"✔️ Informazioni in ({lang_name}) scaricate.")

            self._logger.info(f"ℹ️ Creazione JSON... ({lang_name})")

            # creare dict formattato per esportarlo in JSON
            for id, name_nickname, abilities, icons, skins in zip(
                champ_ids,
                champ_name_nickname,
                champ_abilities,
                champ_icons,
                champ_skins,
            ):

                champ_dict[id] = {
                    "name": name_nickname.get("name"),
                    "nickname": name_nickname.get("nickname"),
                    "icon": icons.get("champ_icon"),
                }

                abilities_dict = {}
                for ability_name, info in abilities.items():
                    abilities_dict[ability_name] = {
                        "name": info.get("name"),
                        "description": info.get("description"),
                        "icon": icons.get(f"{ability_name}_icon"),
                    }

                champ_dict[id]["abilities"] = abilities_dict

                skins_dict = {}
                for index, skin in enumerate(skins):
                    skins_dict[index] = {
                        "name": skin.get("name"),
                        "splash": skin.get("splash"),
                        "loading": skin.get("loading"),
                    }

                champ_dict[id]["skins"] = skins_dict

            if not json_champ_path.exists():
                with open(json_champ_path, "w", encoding="utf-8") as file:
                    dump(champ_dict, file, indent=4, ensure_ascii=False)

            self._logger.info(f"ℹ️ JSON path: {json_champ_path}")
            self._logger.info(f"✅ JSON creato. ({lang_name})")


if __name__ == "__main__":
    api = Extract()

    api.languages_to_json()
    api.data_champs_to_json(countries=("korea",))
