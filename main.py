from datetime import datetime
import time
from colorama import Fore
import requests
import random
from fake_useragent import UserAgent
import asyncio
import json
import gzip
import brotli
import zlib
import chardet
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class blum:
    BASE_URL = "https://user-domain.blum.codes/api/v1/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://telegram.blum.codes",
        "referer": "https://telegram.blum.codes/",
        "priority": "u=1, i", 
        "Content-Type": "application/json",
        "Lang": "en",
        "sec-ch-ua": '"Microsoft Edge";v="134", "Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge WebView2";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()
        self.uid = None
        self.session = self.sessions()

    def banner(self) -> None:
        """BLUM AUTOMATION SCRIPT"""
        self.log("Join Telegram Channel:(https://t.me/D4rkCipherX)", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )
        
    def sessions(self):
        session = requests.Session()
        retries = Retry(total=3,
                        backoff_factor=1,
                        status_forcelist=[500, 502, 503, 504, 520])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def decode_response(self, response):
        """
        Decodes server responses in general.

Parameters:
response: requests.Response object

Returns:
- If Content-Type contains 'application/json', then returns a Python object (dict or list) parsed as JSON.
- If not JSON, then returns the decoded string.
"""
        # Ambil header
        content_encoding = response.headers.get('Content-Encoding', '').lower()
        content_type = response.headers.get('Content-Type', '').lower()

        # Tentukan charset dari Content-Type, default ke utf-8
        charset = 'utf-8'
        if 'charset=' in content_type:
            charset = content_type.split('charset=')[-1].split(';')[0].strip()

        # Ambil data mentah
        data = response.content

        # Dekompresi jika perlu
        try:
            if content_encoding == 'gzip':
                data = gzip.decompress(data)
            elif content_encoding in ['br', 'brotli']:
                data = brotli.decompress(data)
            elif content_encoding in ['deflate', 'zlib']:
                data = zlib.decompress(data)
        except Exception:
            # Jika dekompresi gagal, lanjutkan dengan data asli
            pass

        # Coba decode menggunakan charset yang didapat
        try:
            text = data.decode(charset)
        except Exception:
            # Fallback: deteksi encoding dengan chardet
            detection = chardet.detect(data)
            detected_encoding = detection.get("encoding", "utf-8")
            text = data.decode(detected_encoding, errors='replace')

        # Jika konten berupa JSON, kembalikan hasil parsing JSON
        if 'application/json' in content_type:
            try:
                return json.loads(text)
            except Exception:
                # Jika parsing JSON gagal, kembalikan string hasil decode
                return text
        else:
            return text
        
    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)
        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        # API 1: Login via Telegram Mini App
        login_url = f"{self.BASE_URL}auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        payload = json.dumps({"query": token})
        login_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://telegram.blum.codes",
            "priority": "u=1, i",
            "referer": "https://telegram.blum.codes/"
        }

        try:
            self.log("📡 Sending login request...", Fore.CYAN)
            login_response = requests.post(login_url, headers=login_headers, data=payload)
            login_response.raise_for_status() 
            login_data = self.decode_response(login_response)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during login: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
            except Exception:
                pass
            return

        # Proses respons login agar tidak tampil mentah
        try:
            token_data = login_data.get("token", {})
            access_token = token_data.get("access", "")

            # Simpan token refresh untuk digunakan di API berikutnya
            self.token = access_token

            self.log("✅ Login successful! Processed login response", Fore.GREEN)
        except Exception as e:
            self.log(f"❌ Error processing login response: {e}", Fore.RED)
            return

        # API 2: Mendapatkan informasi user via /user/me
        user_me_url = f"{self.BASE_URL}user/me"
        user_me_headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        try:
            self.log("📡 Sending user info request...", Fore.CYAN)
            user_me_response = requests.get(user_me_url, headers=user_me_headers)
            user_me_response.raise_for_status()
            user_me_data = self.decode_response(user_me_response)

            # Proses respons user/me
            u_id = user_me_data.get("id", {}).get("id", "N/A")
            u_name = user_me_data.get("username", "N/A")
            referrer_token = user_me_data.get("referrerToken", "N/A")
            u_created_at = user_me_data.get("createdAt", "N/A")
            self.uid = u_id

            self.log("👤 User Info:", Fore.GREEN)
            self.log(f"    - ID: {u_id}", Fore.CYAN)
            self.log(f"    - Username: {u_name}", Fore.CYAN)
            self.log(f"    - Referrer Token: {referrer_token}", Fore.CYAN)
            self.log(f"    - Created At: {u_created_at}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch user info: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {user_me_response.text}", Fore.RED)
            except Exception:
                pass
        except Exception as e:
            self.log(f"❌ Unexpected error in user info request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {user_me_response.text}", Fore.RED)
            except Exception:
                pass

        # API 3: Mendapatkan saldo friends via /friends/balance
        friends_balance_url = f"{self.BASE_URL}friends/balance"
        user_balance_headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        try:
            self.log("📡 Sending friends balance request...", Fore.CYAN)
            friends_response = requests.get(friends_balance_url, headers=user_balance_headers)
            friends_response.raise_for_status()
            friends_data = self.decode_response(friends_response)

            # Proses respons friends balance
            limit_inv = friends_data.get("limitInvitation", "N/A")
            used_inv = friends_data.get("usedInvitation", "N/A")
            amount_for_claim = friends_data.get("amountForClaim", "N/A")
            referral_token = friends_data.get("referralToken", "N/A")
            percent_friends = friends_data.get("percentFromFriends", "N/A")
            percent_friends_friends = friends_data.get("percentFromFriendsOfFriends", "N/A")
            can_claim = friends_data.get("canClaim", "N/A")
            enable_new_balance = friends_data.get("enableNewBalance", "N/A")

            self.log("💰 Friends Balance:", Fore.GREEN)
            self.log(f"    - Limit Invitation: {limit_inv}", Fore.CYAN)
            self.log(f"    - Used Invitation: {used_inv}", Fore.CYAN)
            self.log(f"    - Amount For Claim: {amount_for_claim}", Fore.CYAN)
            self.log(f"    - Referral Token: {referral_token}", Fore.CYAN)
            self.log(f"    - Percent From Friends: {percent_friends}", Fore.CYAN)
            self.log(f"    - Percent From Friends Of Friends: {percent_friends_friends}", Fore.CYAN)
            self.log(f"    - Can Claim: {can_claim}", Fore.CYAN)
            self.log(f"    - Enable New Balance: {enable_new_balance}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch friends balance: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {friends_response.text}", Fore.RED)
            except Exception:
                pass
        except Exception as e:
            self.log(f"❌ Unexpected error in friends balance request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {friends_response.text}", Fore.RED)
            except Exception:
                pass
            
        # API 4: Mendapatkan leaderboard
        leaderboard_url = f"{self.BASE_URL}leaderboard/my"
        leaderboard_headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        try:
            self.log("📡 Sending leaderboard request...", Fore.CYAN)
            leaderboard_response = requests.get(leaderboard_url, headers=leaderboard_headers)
            leaderboard_response.raise_for_status()
            leaderboard_data = self.decode_response(leaderboard_response)
            
            bp = leaderboard_data.get("BP", {})
            mp = leaderboard_data.get("MP", {})
            self.log("🏆 Leaderboard Info:", Fore.GREEN)
            self.log(f"    - BP: Position {bp.get('position', 'N/A')}, Amount {bp.get('amount', 'N/A')}", Fore.CYAN)
            self.log(f"    - MP: Position {mp.get('position', 'N/A')}, Amount {mp.get('amount', 'N/A')}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch leaderboard info: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {leaderboard_response.text}", Fore.RED)
            except Exception:
                pass
        except Exception as e:
            self.log(f"❌ Unexpected error in leaderboard request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {leaderboard_response.text}", Fore.RED)
            except Exception:
                pass

        # API 5: Mekanik Auto Join Tribe
        tribe_headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        tribe_my_url = "https://tribe-domain.blum.codes/api/v1/tribe/my"
        already_in_target = False  # Flag untuk cek status tribe
        try:
            self.log("📡 Checking current tribe...", Fore.CYAN)
            tribe_my_response = requests.get(tribe_my_url, headers=tribe_headers)
            tribe_my_response.raise_for_status()
            current_tribe = self.decode_response(tribe_my_response)
            current_chatname = current_tribe.get("chatname", "")
            if current_chatname == "D4rkCipherX":
                self.log("ℹ️ Already in the target tribe.", Fore.GREEN)
                already_in_target = True
            else:
                self.log("🔄 You are in a different tribe. Leaving current tribe...", Fore.YELLOW)
                tribe_leave_url = "https://tribe-domain.blum.codes/api/v1/tribe/leave"
                try:
                    leave_response = requests.post(tribe_leave_url, headers=tribe_headers, json={})
                    leave_response.raise_for_status()
                    self.log("✅ Successfully left the current tribe.", Fore.GREEN)
                except Exception as e:
                    self.log(f"❌ Failed to leave current tribe: {e}", Fore.RED)
                    return
        except requests.exceptions.RequestException:
            self.log("ℹ️ Not currently in any tribe.", Fore.YELLOW)
        except Exception as e:
            self.log(f"❌ Unexpected error when checking tribe: {e}", Fore.RED)
        
        # Jika belum berada di tribe target, maka join ke tribe target
        if not already_in_target:
            tribe_join_url = "https://tribe-domain.blum.codes/api/v1/tribe/6703ab16-0000-4064-8396-72ade0c60141/join"
            try:
                self.log("📡 Sending join tribe request...", Fore.CYAN)
                join_response = requests.post(tribe_join_url, headers=tribe_headers)
                join_response.raise_for_status()
                
                if join_response.status_code == 200:
                    self.log("✅ Successfully joined the tribe!", Fore.GREEN)
                else:
                    self.log(f"❌ Failed to join tribe", Fore.RED)    
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to join tribe: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {join_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"❌ Unexpected error when joining tribe: {e}", Fore.RED)
    
    def daily(self) -> None:
        self.log("🔄 Attempting to check daily reward...", Fore.GREEN)

        daily_url = "https://game-domain.blum.codes/api/v2/daily-reward"
        daily_headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # API 1: GET daily reward info
        try:
            self.log("📡 Sending GET daily reward request...", Fore.CYAN)
            response = requests.get(daily_url, headers=daily_headers)
            response.raise_for_status()
            data = self.decode_response(response)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch daily reward info: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during GET daily reward: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception:
                pass
            return

        try:
            claim_status = data.get("claim", "N/A")
            current_streak = data.get("currentStreakDays", "N/A")
            today_reward = data.get("todayReward", {})
            can_claim_at = data.get("canClaimAt", None)

            self.log("✅ Daily reward info received:", Fore.GREEN)
            self.log(f"    - Claim: {claim_status}", Fore.CYAN)
            self.log(f"    - Current Streak Days: {current_streak}", Fore.CYAN)
            self.log(f"    - Today's Reward: {today_reward}", Fore.CYAN)
            self.log(f"    - Can Claim At: {can_claim_at}", Fore.CYAN)
        except Exception as e:
            self.log(f"❌ Error processing daily reward info: {e}", Fore.RED)
            return

        # Jika claim_status bernilai "unavailable", jangan klaim daily reward
        if isinstance(claim_status, str) and claim_status.lower() == "unavailable":
            self.log("🚫 Daily reward claim is unavailable. Skipping claim.", Fore.YELLOW)
            return

        # Langsung claim daily reward tanpa memeriksa waktu
        try:
            self.log("🚀 Claiming daily reward...", Fore.CYAN)
            claim_response = requests.post(daily_url, headers=daily_headers)
            claim_response.raise_for_status()
            claim_data = self.decode_response(claim_response)
            self.log("✅ Daily reward claimed successfully:", Fore.GREEN)
            self.log(f"    - Response: {claim_data}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to claim daily reward: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during claiming daily reward: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
            except Exception:
                pass
            return

        # Cek saldo reward teman (friend balance) setelah claim daily reward
        friends_balance_url = "https://wallet-domain.blum.codes/api/v1/friends/balance"
        try:
            self.log("📡 Checking friend reward balance...", Fore.CYAN)
            fb_response = requests.get(friends_balance_url, headers=daily_headers)
            fb_response.raise_for_status()
            fb_data = self.decode_response(fb_response)
            amount = fb_data.get("amount", "N/A")
            can_claim = fb_data.get("canClaim", False)
            can_claim_at = fb_data.get("canClaimAt", None)
            self.log("✅ Friend reward balance info received:", Fore.GREEN)
            self.log(f"    - Amount: {amount}", Fore.CYAN)
            self.log(f"    - Can Claim: {can_claim}", Fore.CYAN)
            self.log(f"    - Can Claim At: {can_claim_at}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch friend reward balance: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {fb_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during GET friend reward balance: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {fb_response.text}", Fore.RED)
            except Exception:
                pass
            return

        # Jika friend reward dapat di-claim, maka lakukan claim
        if can_claim:
            friends_claim_url = "https://wallet-domain.blum.codes/api/v1/friends/claim"
            try:
                self.log("🚀 Claiming friend reward...", Fore.CYAN)
                friends_claim_response = requests.post(friends_claim_url, headers=daily_headers)
                friends_claim_response.raise_for_status()
                friends_claim_data = self.decode_response(friends_claim_response)
                self.log("✅ Friend reward claimed successfully:", Fore.GREEN)
                self.log(f"    - Claimed Amount: {friends_claim_data.get('amount', 'N/A')}", Fore.CYAN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to claim friend reward: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {friends_claim_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"❌ Unexpected error during claiming friend reward: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {friends_claim_response.text}", Fore.RED)
                except Exception:
                    pass
        else:
            self.log("🚫 Friend reward cannot be claimed at this time.", Fore.YELLOW)
        
    def task(self) -> None:
        import time
        import json
        import requests

        self.log("🚀 Fetching tasks...", Fore.GREEN)
        tasks_url = "https://earn-domain.blum.codes/api/v1/tasks"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # Ambil mapping keyword dari GitHub
        task_json_url = "https://raw.githubusercontent.com/livexords-nw/blum-bot/refs/heads/main/task.json"
        try:
            self.log("🔑 Loading task keyword mapping from GitHub...", Fore.GREEN)
            task_response = requests.get(task_json_url)
            task_response.raise_for_status()
            keyword_mapping = task_response.json()
            self.log("✅ Loaded task keyword mapping from GitHub", Fore.GREEN)
        except Exception as e:
            self.log(f"❌ Failed to load task keyword mapping from GitHub: {e}", Fore.RED)
            keyword_mapping = {}

        # Ambil daftar tasks
        try:
            tasks_response = requests.get(tasks_url, headers=headers)
            tasks_response.raise_for_status()
            tasks_list = tasks_response.json()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch tasks: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {tasks_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error when fetching tasks: {e}", Fore.RED)
            return

        self.log(f"✅ Fetched tasks. Total sections: {len(tasks_list)}", Fore.GREEN)
        
        # Ekstrak semua tasks (termasuk subTasks dan subSections)
        tasks_to_process = []

        def extract_tasks(section: dict) -> None:
            if "tasks" in section and isinstance(section["tasks"], list):
                for task in section["tasks"]:
                    tasks_to_process.append(task)
                    if "subTasks" in task and isinstance(task["subTasks"], list):
                        for sub in task["subTasks"]:
                            tasks_to_process.append(sub)
            if "subSections" in section and isinstance(section["subSections"], list):
                for sub_section in section["subSections"]:
                    extract_tasks(sub_section)

        for section in tasks_list:
            extract_tasks(section)

        self.log(f"👉 Found {len(tasks_to_process)} tasks in total.", Fore.GREEN)

        # Kategorisasi task berdasarkan status
        tasks_to_start = []
        tasks_to_verify = []
        tasks_to_claim = []

        for task_item in tasks_to_process:
            status = task_item.get("status", "").upper()
            sub_type = task_item.get("subType", "").upper()
            if status == "NOT_STARTED" and sub_type != "FARMING" and sub_type != "REFERRAL" and sub_type != "MEMEPAD_TOKEN_TRADE":
                tasks_to_start.append(task_item)
            elif status == "READY_FOR_VERIFY":
                tasks_to_verify.append(task_item)
            elif status == "READY_FOR_CLAIM":
                tasks_to_claim.append(task_item)
            else:
                self.log(f"ℹ️ Task {task_item.get('id')} has status '{status}' - no action required.", Fore.YELLOW)

        self.log(f"👉 Tasks to start: {len(tasks_to_start)}", Fore.GREEN)
        self.log(f"👉 Tasks to verify: {len(tasks_to_verify)}", Fore.GREEN)
        self.log(f"👉 Tasks to claim: {len(tasks_to_claim)}", Fore.GREEN)

        # 1. Proses task dengan status NOT_STARTED: Start task
        for task_item in tasks_to_start:
            task_id = task_item.get("id")
            if not task_id:
                continue
            start_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/start"
            try:
                self.log(f"🚀 Starting task {task_id}...", Fore.CYAN)
                start_response = requests.post(start_url, headers=headers)
                start_response.raise_for_status()
                self.log(f"✅ Task {task_id} started.", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to start task {task_id}: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {start_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"❌ Unexpected error when starting task {task_id}: {e}", Fore.RED)

        # 2. Proses task dengan status READY_FOR_VERIFY: Verify task
        for task_item in tasks_to_verify:
            task_id = task_item.get("id")
            if not task_id:
                continue
            verify_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/validate"
            payload = {}
            if task_item.get("validationType", "").upper() == "KEYWORD":
                # Cari keyword dari mapping yang diambil dari GitHub
                keyword = keyword_mapping.get(task_id)
                if keyword:
                    payload = {"keyword": keyword}
                else:
                    self.log(f"❌ Keyword not found for task {task_id} in mapping.", Fore.RED)
                    continue  # Lewati verifikasi jika keyword tidak ditemukan
            try:
                self.log(f"🛠 Verifying task {task_id}...", Fore.CYAN)
                if payload:
                    verify_response = requests.post(verify_url, headers=headers, json=payload)
                else:
                    verify_response = requests.post(verify_url, headers=headers)
                verify_response.raise_for_status()
                verify_data = verify_response.json()
                self.log(f"✅ Task {task_id} verified. Response: {verify_data}", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to verify task {task_id}: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {verify_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"❌ Unexpected error when verifying task {task_id}: {e}", Fore.RED)

        # Delay 5 detik sebelum claim
        self.log("⏳ Waiting 5 seconds before claiming tasks...", Fore.YELLOW)
        time.sleep(5)

        # 3. Proses task dengan status READY_FOR_CLAIM: Claim task
        for task_item in tasks_to_claim:
            task_id = task_item.get("id")
            if not task_id:
                continue
            claim_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/claim"
            try:
                self.log(f"💰 Claiming task {task_id}...", Fore.CYAN)
                claim_response = requests.post(claim_url, headers=headers)
                claim_response.raise_for_status()
                claim_data = claim_response.json()
                self.log(f"✅ Task {task_id} claimed. Response: {claim_data}", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to claim task {task_id}: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"❌ Unexpected error when claiming task {task_id}: {e}", Fore.RED)
                
    def farming(self) -> None:
        import time
        import requests

        self.log("🚜 Starting farming process...", Fore.GREEN)
        
        # Header yang akan digunakan (authorization ditambahkan)
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        
        # Step 1: Ambil informasi wallet points balance
        balance_url = "https://wallet-domain.blum.codes/api/v1/wallet/my/points/balance"
        try:
            self.log("📡 Fetching wallet points balance...", Fore.CYAN)
            balance_response = requests.get(balance_url, headers=headers)
            balance_response.raise_for_status()
            balance_data = self.decode_response(balance_response)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch wallet points balance: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {balance_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error fetching wallet points balance: {e}", Fore.RED)
            return

        # Cari data Blum points berdasarkan currencyId yang spesifik
        blum_points = None
        for point in balance_data.get("points", []):
            if point.get("currencyId") == "59bee2e3-a682-4ec5-93df-a3bb294f7bed":
                blum_points = point
                break
        if not blum_points:
            self.log("❌ Blum points data not found in wallet points balance.", Fore.RED)
            return

        # Ekstrak informasi farming dari Blum points
        farming_info = blum_points.get("farming")
        if not farming_info:
            self.log("❌ Farming info not available in Blum points data. Starting farming session...", Fore.YELLOW)
            # Jika tidak ada farming_info, langsung mulai sesi farming
            start_url = "https://wallet-domain.blum.codes/api/v1/farming/start"
            try:
                self.log("🚜 Starting farming session...", Fore.CYAN)
                start_response = requests.post(start_url, headers=headers)
                start_response.raise_for_status()
                start_data = self.decode_response(start_response)
                self.log("✅ Farming session started:", Fore.GREEN)
                self.log(f"    - Start Time: {start_data.get('startTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - End Time: {start_data.get('endTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - Current Time: {start_data.get('currentTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - Earnings Rate: {start_data.get('earningsRate', 'N/A')}", Fore.CYAN)
                self.log(f"    - Balance: {start_data.get('balance', 'N/A')}", Fore.CYAN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to start farming session: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {start_response.text}", Fore.RED)
                except Exception:
                    pass
            return

        start_time = farming_info.get("startTime", "N/A")
        end_time = farming_info.get("endTime", "N/A")
        server_current_time = farming_info.get("currentTime", "N/A")
        earnings_rate = farming_info.get("earningsRate", "N/A")
        farming_balance = farming_info.get("balance", "N/A")
        
        self.log("📊 Farming Info:", Fore.GREEN)
        self.log(f"    - Start Time: {start_time}", Fore.CYAN)
        self.log(f"    - End Time: {end_time}", Fore.CYAN)
        self.log(f"    - Server Current Time: {server_current_time}", Fore.CYAN)
        self.log(f"    - Earnings Rate: {earnings_rate}", Fore.CYAN)
        self.log(f"    - Farming Balance: {farming_balance}", Fore.CYAN)

        # Gunakan waktu dari device (dalam ms)
        current_device_time = int(time.time() * 1000)
        self.log(f"⏰ Device current time: {current_device_time}", Fore.CYAN)
        
        try:
            end_time_int = int(end_time)
        except Exception:
            self.log("❌ Invalid end time in farming info.", Fore.RED)
            return

        # Jika waktu device sudah mencapai atau melebihi endTime, klaim farming reward
        if current_device_time >= end_time_int:
            claim_url = "https://wallet-domain.blum.codes/api/v1/farming/claim"
            try:
                self.log("🚜 Claiming farming reward...", Fore.CYAN)
                claim_response = requests.post(claim_url, headers=headers)
                claim_response.raise_for_status()
                claim_data = self.decode_response(claim_response)
                self.log("✅ Farming reward claimed:", Fore.GREEN)
                self.log(f"    - Available Balance: {claim_data.get('availableBalance', 'N/A')}", Fore.CYAN)
                self.log(f"    - Play Passes: {claim_data.get('playPasses', 'N/A')}", Fore.CYAN)
                self.log(f"    - Is Fast Farming Enabled: {claim_data.get('isFastFarmingEnabled', 'N/A')}", Fore.CYAN)
                self.log(f"    - Timestamp: {claim_data.get('timestamp', 'N/A')}", Fore.CYAN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to claim farming reward: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
                except Exception:
                    pass
                
            # Jika belum waktunya untuk klaim, mulai sesi farming baru
            start_url = "https://wallet-domain.blum.codes/api/v1/farming/start"
            try:
                self.log("🚜 Starting farming session...", Fore.CYAN)
                start_response = requests.post(start_url, headers=headers)
                start_response.raise_for_status()
                start_data = self.decode_response(start_response)
                self.log("✅ Farming session started:", Fore.GREEN)
                self.log(f"    - Start Time: {start_data.get('startTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - End Time: {start_data.get('endTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - Current Time: {start_data.get('currentTime', 'N/A')}", Fore.CYAN)
                self.log(f"    - Earnings Rate: {start_data.get('earningsRate', 'N/A')}", Fore.CYAN)
                self.log(f"    - Balance: {start_data.get('balance', 'N/A')}", Fore.CYAN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to start farming session: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {start_response.text}", Fore.RED)
                except Exception:
                    pass

    def game(self) -> None:

        # Define color aliases
        green = Fore.GREEN
        white = Fore.WHITE
        red = Fore.RED
        cyan = Fore.CYAN
        yellow = Fore.YELLOW

        self.log("🎮 Starting game process...", green)

        # Prepare headers using self.HEADERS and token from self.token
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # API endpoints
        balance_url = "https://wallet-domain.blum.codes/api/v1/wallet/my/points/balance"
        play_url = "https://game-domain.blum.codes/api/v2/game/play"
        claim_url = "https://game-domain.blum.codes/api/v2/game/claim"

        # Main loop: continue playing until no tickets remain
        while True:
            # Fetch wallet points balance
            try:
                self.log("📡 Fetching wallet points balance...", cyan)
                balance_response = requests.get(balance_url, headers=headers)
                balance_response.raise_for_status()
                balance_data = self.decode_response(balance_response)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to fetch wallet points balance: {e}", red)
                try:
                    self.log(f"📄 Response content: {balance_response.text}", red)
                except Exception:
                    pass
                break
            except Exception as e:
                self.log(f"❌ Unexpected error fetching wallet points balance: {e}", red)
                break

            # Find Play passes data based on specific currencyId
            play_passes = None
            for point in balance_data.get("points", []):
                if point.get("currencyId") == "2fcd0259-9086-474b-80f6-88c66c4f9e74":
                    play_passes = point
                    break
            if play_passes is None:
                self.log("❌ Play passes data not found in wallet points balance.", red)
                break

            try:
                ticket_count = float(play_passes.get("balance", "0"))
            except Exception:
                self.log("❌ Failed to parse Play passes balance.", red)
                break

            if ticket_count <= 0:
                self.log("🚫 No game tickets available. Exiting game loop.", red)
                break

            self.log(f"{green}You have {white}{ticket_count}{green} game ticket(s) available.", green)

            # Initiate a new game session
            try:
                self.log("🎮 Initiating game play...", cyan)
                game_response = requests.post(play_url, headers=headers)
                game_response.raise_for_status()
                game_data = self.decode_response(game_response)
                game_id = game_data.get("gameId")
                if not game_id:
                    self.log("❌ Game ID not found in game play response.", red)
                    break
                self.log(f"✅ Game play initiated. Game ID: {white}{game_id}", green)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to initiate game play: {e}", red)
                try:
                    self.log(f"📄 Response content: {game_response.text}", red)
                except Exception:
                    pass
                break
            except Exception as e:
                self.log(f"❌ Unexpected error during game play: {e}", red)
                break

            # Wait a random duration between 30 and 38 seconds before claiming the game
            wait_time = random.randint(30, 38)
            self.log(f"⏳ Waiting for {white}{wait_time}{cyan} seconds before claiming the game...", cyan)
            time.sleep(wait_time)

            # Define a function to claim the game using the stored game_id
            def claim_game():
                try:
                    points = random.randint(self.config.get("low_point", 260), self.config.get("high_point", 280))
                    freeze = random.randint(1, 2)
                    payload = json.dumps({
                        "game_id": game_id,
                        "points": points,
                        "freeze": freeze
                    })
                    self.log("🔐 Creating payload for claim...", cyan)
                    _headers = {
                        "User-Agent": UserAgent().random,
                        "Content-Type": "application/json",
                    }
                    res_payload = requests.post("https://blum-payload.sdsproject.org", headers=_headers, data=payload)
                    res_payload.raise_for_status()

                    # Send claim request with the encrypted payload
                    res = requests.post(claim_url, headers=headers, data=res_payload.text)
                    res.raise_for_status()
                    return res, points
                except Exception as e:
                    self.log(f"❌ Error in claim_game: {e}", red)
                    return None, None

            # Loop to attempt claim until a valid result is obtained for the same game session
            while True:
                res, points = claim_game()
                if res is None:
                    self.log("❌ Failed to claim game, retrying...", red)
                    time.sleep(5)
                    continue

                if "OK" in res.text:
                    self.log(f"🎉 Successfully earned {white}{points}{green} points from the game!", green)
                    ticket_count -= 1
                    self.log(f"🎟️ Remaining game ticket(s): {white}{ticket_count}", green)
                    break

                try:
                    message_raw = self.decode_response(res)
                    message = message_raw.get("message","")
                except Exception:
                    message = ""
                if message == "game session not finished":
                    self.log("⌛ Game session not finished, retrying claim...", yellow)
                    time.sleep(5)
                    continue
                if message == "game session not found":
                    self.log("🚫 Game session not found, game ended.", red)
                    break
                if message == "Token is invalid":
                    self.log("🔑 Token is invalid, re-authenticating...", red)
                    self.login()  # Re-login to obtain a new token
                    headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
                    continue

                self.log(f"❌ Failed to earn {white}{points}{red} points from the game!", red)
                break

            # End of the game session; loop continues until game tickets are 0

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        import random
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

async def process_account(account, original_index, account_label, blu, config):
    # Menampilkan informasi akun
    display_account = account[:10] + "..." if len(account) > 10 else account
    blu.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)
    
    # Override proxy jika diaktifkan
    if config.get("proxy", False):
        blu.override_requests()
    else:
        blu.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)
    
    # Login (fungsi blocking, dijalankan di thread terpisah) dengan menggunakan index asli (integer)
    await asyncio.to_thread(blu.login, original_index)
    
    blu.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "daily": "Daily Reward Check & Claim 🎁",
        "task": "Automatically solving tasks 🤖",
        "farming": "Automatic farming for abundant harvest 🌾",
        "game": "Play exciting game and earn points 🎮",
    }
    
    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        blu.log(f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}", color)
        if task_status:
            blu.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(blu, task_key))
    
    delay_switch = config.get("delay_account_switch", 10)
    blu.log(f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.", Fore.CYAN)
    await asyncio.sleep(delay_switch)

async def worker(worker_id, blu, config, queue):
    """
Each worker will take one account from the queue and process them sequentially.
The worker will not take a new account until the previous account has finished processing.
"""
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, blu, config)
        queue.task_done()
    blu.log(f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN)

async def main():
    blu = blum()  # Inisialisasi instance class blum Anda
    config = blu.load_config()
    all_accounts = blu.query_list
    num_threads = config.get("thread", 1)  # Jumlah worker sesuai konfigurasi
    
    if config.get("proxy", False):
        proxies = blu.load_proxies()
    
    blu.log("=== D4rkCipherX ===", Fore.YELLOW)
    blu.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)
    
    while True:
        # Buat queue baru dan masukkan semua akun (dengan index asli)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))
        
        # Buat task worker sesuai dengan jumlah thread yang diinginkan
        workers = [asyncio.create_task(worker(i+1, blu, config, queue)) for i in range(num_threads)]
        
        # Tunggu hingga semua akun di queue telah diproses
        await queue.join()
        
        # Opsional: batalkan task worker (agar tidak terjadi tumpang tindih)
        for w in workers:
            w.cancel()
        
        blu.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        blu.log(f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.", Fore.CYAN)
        await asyncio.sleep(delay_loop)

if __name__ == "__main__":
    asyncio.run(main())