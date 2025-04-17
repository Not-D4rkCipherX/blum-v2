## BLUM BOT

## BOT FEATURE

- Auto Play Game
- Auto Claim Daily
- Auto Task
- Auto farming
- Multi Account
- Proxy Support

## COMMANDS
1. **Install older python version for termux**
```
   pkg update && pkg upgrade
```
```
   pkg install clang cmake ninja rust make
```
```
   pkg install tur-repo
```
```
   pkg install python3.10
```
```
   pip3.10 install --upgrade pip wheel
```
2. **Script Installation**
   ```bash
   git clone https://github.com/Not-D4rkCipherX/blum-v2.git
   cd blum-v2
   pip3.10 install -r requirements.txt
   ```
3. **Configuration**
To Adjust GamePoint, Enable/Disble Tasks, etc..
```bash
nano config.json
```
```json
{
  "game": true,
  "daily": true,
  "task": true,
  "farming": true,
  "low_point": 260,
  "high_point": 280,
  "thread": 1,
  "proxy": false,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```
4. **ADD ACCOUNTS**
   ```
   nano query.txt
   ```
   
5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.
   
6. **START THE BOT**
```bash
python3.10 main.py
```
## Buy ME a Coffee

- **EVM:** 0x47f41Fcb17cF9B7A02C26EE855d26bB8D3928E1b
- **TON:** UQA-qG5eyQ7gVxvPDpy484xzc0UPS9a8hJsUAwe0T_3D7_oF
- **SOL:** A1pUv13rRDtubtYJuXswZYSQBJojPhthXJftfNZBRnEX
- **SUI:** 0xeb697918d66c4ade867d61d0b8fb541df83675e8f60b6b81da8917aab149ee8f

**D4rkCipherX**
