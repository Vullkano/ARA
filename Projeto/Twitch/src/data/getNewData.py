import requests
import pandas as pd
import pathlib
from pathlib import Path
import time
from datetime import datetime  # Import necessário para o formato de data

def getData(country: str, current_dir: pathlib.WindowsPath, CLIENT_ID: str, OAUTH_TOKEN: str):
    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]

    if country not in countries:
        raise ValueError(f"País '{country}' não é válido. Países disponíveis: {', '.join(countries)}.")

    if type(current_dir) != pathlib.WindowsPath or "Twitch" not in str(current_dir):
        raise ValueError("O diretório especificado não é válido ou não contém 'Twitch' no caminho.")

    while current_dir.name != "Twitch":
        current_dir = current_dir.parent

    current_dir_data = current_dir / "data"

    Filetarget = "musae_" + country + "_target.csv"
    targetPath = current_dir_data / country / Filetarget

    if not targetPath.exists():
        raise FileNotFoundError(f"Ficheiro {targetPath} não encontrado.")

    nodos_df = pd.read_csv(targetPath)

    user_idList = []
    usernameList = []
    created_atList = []
    profile_picList = []
    broadcaster_typeList = []
    game_nameList = []

    qtd = 0

    for user_id in nodos_df['id']:
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {OAUTH_TOKEN}'
        }

        # https://dev.twitch.tv/docs/api/reference/#get-channel-information
        try:
            user_url = f'https://api.twitch.tv/helix/users?id={user_id}'
            user_response = requests.get(user_url, headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()

            if user_data['data']:
                user_info = user_data['data'][0]
                username = user_info.get('display_name', None)
                created_at_raw = user_info.get('created_at', None)
                if created_at_raw:
                    created_at = datetime.strptime(created_at_raw, '%Y-%m-%dT%H:%M:%SZ').date()
                else:
                    created_at = None
                profile_pic = user_info.get('profile_image_url', None)
                broadcaster_type = user_info.get('broadcaster_type', None)
            else:
                username = created_at = profile_pic = broadcaster_type = None

            channel_url = f'https://api.twitch.tv/helix/channels?broadcaster_id={user_id}'
            channel_response = requests.get(channel_url, headers=headers)
            channel_response.raise_for_status()
            channel_data = channel_response.json()

            # TODO Só agr é que vi que existe -> content_classification_labels
            print(channel_data)

            if channel_data['data']:
                game_name = channel_data['data'][0].get('game_name', None)
            else:
                game_name = None

            print(
                f"{country} - {qtd}: Utilizador: {username} | Criado em: {created_at} | Tipo: {broadcaster_type} | Jogo: {game_name} | Imagem: {profile_pic}"
            )

            user_idList.append(user_id)
            usernameList.append(username)
            created_atList.append(created_at)
            profile_picList.append(profile_pic)
            broadcaster_typeList.append(broadcaster_type)
            game_nameList.append(game_name)
            qtd += 1

        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ao fazer requisição: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Erro ao fazer requisição: {req_err}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

        time.sleep(0.1)

    new_columns = pd.DataFrame({
        "id": user_idList,
        "username": usernameList,
        "created_at": created_atList,
        "profile_pic": profile_picList,
        "broadcaster_type": broadcaster_typeList,
        "game_name": game_nameList
    })

    new_df = pd.merge(nodos_df, new_columns, on="id", how="left")
    NewFiletarget = "Raw_musae_" + country + "_target.csv"

    # Definir o nome da nova pasta
    new_folder_name = "processed_data"

    # Caminho para a nova pasta
    newPath = current_dir_data / 'data' / country / new_folder_name / NewFiletarget

    # Criar a nova pasta se ela não existir
    newPath.mkdir(parents=True, exist_ok=True)

    # Salvar o DataFrame limpo no novo diretório
    new_df.to_csv(newPath, index=False)
    print(f"Dados salvos em: {newPath}")


if __name__ == "__main__":
    # https://twitchtokengenerator.com/
    CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
    OAUTH_TOKEN = 'e1b1lyolmag5m6rhgzsa8efwx9d7zq'

    countries = ["PTBR", "DE", "ENGB", "ES", "FR", "RU"]
    current_dir = Path.cwd()

    for country in countries:
        getData(country, current_dir, CLIENT_ID, OAUTH_TOKEN)