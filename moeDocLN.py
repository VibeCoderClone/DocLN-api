from curl_cffi import requests
from re import search, findall
from time import time
# this thing for some reason took the most time lmao

# Mapping
TheLoai = {
  "Action": 1,
  "Adapted to Anime": 49,
  "Adapted to Drama CD": 51,
  "Adapted to Manga": 50,
  "Adapted to Manhua": 64,
  "Adapted to Manhwa": 65,
  "Adult": 28,
  "Adventure": 2,
  "Age Gap": 52,
  "Boys Love": 60,
  "Character Growth": 54,
  "Chinese Novel": 39,
  "Comedy": 3,
  "Cooking": 43,
  "Different Social Status": 56,
  "Drama": 4,
  "Ecchi": 5,
  "English Novel": 40,
  "Fanfiction": 62,
  "Fantasy": 6,
  "Female Protagonist": 59,
  "Game": 45,
  "Gender Bender": 7,
  "Harem": 8,
  "Historical": 35,
  "Horror": 9,
  "Incest": 10,
  "Isekai": 30,
  "Josei": 33,
  "Korean Novel": 34,
  "Magic": 44,
  "Martial Arts": 37,
  "Mature": 27,
  "Mecha": 11,
  "Military": 36,
  "Misunderstanding": 58,
  "Mystery": 12,
  "Netorare": 32,
  "One shot": 38,
  "Otome Game": 46,
  "Parody": 61,
  "Psychological": 23,
  "Reverse Harem": 47,
  "Romance": 22,
  "Satire": 66,
  "School Life": 13,
  "Science Fiction": 14,
  "Seinen": 31,
  "Shoujo": 15,
  "Shoujo ai": 16,
  "Shounen": 26,
  "Shounen ai": 17,
  "Slice of Life": 18,
  "Slow Life": 55,
  "Sports": 19,
  "Super Power": 24,
  "Supernatural": 20,
  "Suspense": 25,
  "Tragedy": 21,
  "Wars": 53,
  "Web Novel": 29,
  "Workplace": 57,
  "Yandere": 63,
  "Yuri": 48
}
TrangThai = {
    "Đang tiến hành": 1,
    "Tạm ngừng": 2,
    "Đã hoàn thành": 3
}
Loai = {
    "Truyện Dịch": 1,
    "AI Dịch": 2,
    "Sáng tác": 3
}

isDebug = False
def log(msg):
    if isDebug: print(f"[DBG]: {msg}")


class moeDocLN:
    class Authentication:
        @staticmethod
        def retrieve_larvile_token(url: str, login_cookies: dict = {}) -> dict: 
            """
                Retrieve Larvile token, return token as str.
            """
            page = requests.get(url, impersonate="chrome131", cookies=login_cookies)
            pageHTML = page.text
            #Pattern!!
            tokenMatch = search(r"""<input[^>]*name="_token"[^>]*value="([^"]+)"[^>]*>""", pageHTML)
            if not tokenMatch:
                log("Failed on pattern check 456456456456456456456456")
                raise Exception("Failed to retrieve larvile token")
            token = tokenMatch.group(1)
            return {"token": token, "cookies": page.cookies.get_dict()}
        @staticmethod 
        def get_login_cookies(username: str, password: str, isTemporary = False) -> str:
            """
                ... return login cookies as dict
            """
            start = time()
            # Retrieve Token using tricks :)
            loginPage = requests.get('https://docln.sbs/login', impersonate="chrome131")
            cookies = loginPage.cookies
            pageHTML = loginPage.text
            #Pattern!!
            tokenMatch = search(r"""<input[^>]*name="_token"[^>]*value="([^"]+)"[^>]*>""", pageHTML)
            if not tokenMatch:
                log("Failed on pattern check 123123231321321321321213321")

                return "E2"

            token = tokenMatch.group(1)

            # Login to docln.sbs and return the cookies
            formData = {'_token': token, 'name': username, 'password': password, 'remember': 'on'}
            log(formData)
            if isTemporary == False:
                del formData["remember"]
            response = requests.post('https://docln.sbs/login', impersonate="chrome131", data=formData, cookies=cookies)
            if response.status_code == 200:
                all_the_Set_cookies = response.cookies.get_dict()
                end = time()
                log(f"Login took {end - start} s")
                return all_the_Set_cookies
            else:
                log("Failed on status check")
                return "E1"
    
    class NovelsActions:
        @staticmethod
        def create_novel_entry(login_cookies: dict, title: str, author: str, illustrator: str, genres: list, summary: str, extra: str, type_: int = 2, group_id: int = 1, altname: str = '', is_mature: int = 0, status: int = 2) -> int:
            token = moeDocLN.Authentication.retrieve_larvile_token('https://docln.sbs/action/series/create', login_cookies)
            base = [
                ("_token", token["token"]),
                ("title", title),
                ("altname", altname),
                ("author", author),
                ("illustrator", illustrator),
                ("cover", ""),
                ("type", type_),
                ("group_id", group_id),

            ]

            for genre in genres:
                if genre in TheLoai:
                    base.append(("genres[]", TheLoai[genre]))

            base.append(("summary", summary))
            base.append(("extra", extra))
            base.append(("status", status))
            response = requests.post('https://docln.sbs/action/series/store', impersonate="chrome131", cookies=login_cookies | token["cookies"], data=base)

            if response.status_code == 200:
                return True
            else:
                return False
        
        @staticmethod
        def get_series_id(login_cookies: dict, title: str) -> int:
            pass


        @staticmethod
        def edit_novel_entry(login_cookies: dict, series_id: int, title: str, altname: str, author: str, illustrator: str, summary: str, genres: list, status: str, extra: str) -> bool:
            token = moeDocLN.Authentication.retrieve_larvile_token(f'https://docln.sbs/action/series/{series_id}/edit', login_cookies)
            response = requests.post('https://docln.sbs/action/series/update', impersonate="chrome131", cookies=login_cookies | token["cookies"], data={'_token': token["token"], 'series_id': series_id, 'title': title, 'altname': altname, 'cover': '', 'author': author, 'illustrator': illustrator, 'group_id': 1, 'genres[]': genres, 'summary': summary, 'status': status, 'extra': extra})
            return response.status_code == 200
        
        @staticmethod
        def update_cover(cover_path: str, series_id, login_cookies: dict) -> bool:
            token = moeDocLN.Authentication.retrieve_larvile_token(f'https://docln.sbs/action/series/{series_id}/edit', login_cookies)
            with open(cover_path, 'rb') as cover_file:
                files = {'cover': (cover_path, cover_file, 'application/octet-stream')}
                response = requests.post('https://docln.sbs/action/series/update', impersonate="chrome131", cookies=login_cookies | token["cookies"], data={'_token': token["token"], 'series_id': series_id}, files=files)
                return response.status_code == 200

        @staticmethod
        def delete_novel_entry(login_cookies: dict, series_id: int) -> bool:
            token = moeDocLN.Authentication.retrieve_larvile_token(f'https://docln.sbs/action/series/{series_id}/delete', login_cookies)
            response = requests.post('https://docln.sbs/action/series/destroy', impersonate="chrome131", cookies=login_cookies | token["cookies"], data={'_token': token["token"], 'series_id': series_id, 'delete_reason': 'Deleted via moeDocLN library.'})
            return response.status_code == 200

    class BookActions:
        @staticmethod
        #Please make this into a dict later
        def get_book_id(login_cookies: dict, series_id: int) -> list:
            #get book id etc etc, priority : HIGH
            page = requests.get(f'https://docln.sbs/action/series/{series_id}/manage', impersonate="chrome131", cookies=login_cookies) 
            pageHTML = page.text
            #Search for book ids
            book_id_matches = findall(r"""<div[^>]*id="book-(\d+)"[^>]*x-data="[^"]*expanded[^"]*false[^"]*search[^"]*''[^"]*"[^>]*>""", pageHTML)
            return book_id_matches
        
        @staticmethod
        def create_book_entry(login_cookies: dict, series_id: int, title: str) -> bool:
            # Get Token, priority : MEDIUM
            token = moeDocLN.Authentication.retrieve_larvile_token(f'https://docln.sbs/action/book/create/series={series_id}', login_cookies) # weird
            response = requests.post(f'https://docln.sbs/action/book/store', impersonate="chrome131", cookies=login_cookies | token["cookies"], data={'_token': token["token"], 'series_id': series_id, 'title': title, 'download': ''})
            return response.status_code == 200
    
    class ChapterActions:
        @staticmethod
        def create_chapter_entry(login_cookies: dict, book_id: int, title: str, content: str = "") -> bool:
            # Get Token, priority : MEDIUM
            token = moeDocLN.Authentication.retrieve_larvile_token(f'https://docln.sbs/action/chapter/create/book={book_id}', login_cookies) # weird
            response = requests.post(f'https://docln.sbs/action/chapter/store', impersonate="chrome131", cookies=login_cookies | token["cookies"], data={'_token': token["token"], 'book_id': book_id, 'title': title, 'complete': 1, 'image': ("", b"", "application/octet-stream"), 'content': content})
            return response.status_code == 200
        
        #Cannot test this right now.
        @staticmethod
        def create_note_entry(login_cookies: dict, book_id: int, content: str, larvile_token: str) -> int:
            # Get Token, priority : LOW
            token = larvile_token # weird
            response = requests.post(f'https://docln.sbs/action/note/store', impersonate="chrome131", cookies=login_cookies, data={'_token': token, 'content': content, 'book_id': book_id})
            
            if response.status_code == 200:
                note_id_match = search(r'"note_id":\s*(\d+)', response.text)
                if note_id_match:
                    return int(note_id_match.group(1))
                else:
                    return -1
            else:
                return -1

