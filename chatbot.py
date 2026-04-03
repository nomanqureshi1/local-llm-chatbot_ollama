import requests, json,os
from datetime import datetime

ollama = 'http://localhost:11434'

class chatbot:
    def __init__(self, model='llama3.1:8b', temperature=0.7,sys_prompt="You are a helpfull assistant."):
        self.model=model
        self.temperature=temperature
        self.system_prompt=sys_prompt
        self.messages=[{"role":"system","content":self.system_prompt}]
        
        
    def chat(self,user_input):
        self.messages.append({"role":"user","content":user_input})
        response=requests.post(
            f'{ollama}/api/chat/',
           json={
                "model": self.model,
                "messages": self.messages,
                "stream": True,
                "options": {"temperature": self.temperature}
            },
           stream=True
        )
        
        
        
        full_response=""
        for line in response.iter_lines():
            if line:
                chunk=json.loads(line)
                token = chunk.get('message', {}).get('content', '')
                full_response+=token
                print(token, end='', flush=True)
                if chunk.get("done",False):
                    break
        print()
        
        self.messages.append({"role":"assistant","content":full_response})
        return full_response
    
    
    def save(self, filename=None):
        if not filename:
            filename = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("conversations", exist_ok=True)
        with open(f"conversations/{filename}", "w") as f:
            json.dump({"model": self.model, "temperature": self.temperature, "messages": self.messages}, f, indent=2)
        print(f"Saved to conversations/{filename}")
    
    def handle_command(self, cmd):
        parts = cmd.split(maxsplit=1)
        arg = parts[1] if len(parts) > 1 else ''
        c = parts[0].lower()
        if c == '/model':
            self.model = arg or 'llama3.1:8b'
            print(f'Model: {self.model}')
        elif c == '/temp':
            self.temperature = float(arg) if arg else 0.7
            print(f'Temperature: {self.temperature}')
        elif c == '/system':
            self.system_prompt = arg
            self.messages = [{'role':'system','content':arg}]
            print('System prompt updated. Conversation cleared.')
        elif c == '/save': self.save(arg or None)
        elif c == '/clear':
            self.messages = [{'role':'system','content':self.system_prompt}]
            print('Conversation cleared.')
        elif c == '/help':
            print('/model <name>, /temp <0-2>, /system <prompt>,',
                  '/save [file], /clear, /quit')
        elif c == '/quit': return False
        return True




def main():
    bot =chatbot()
    print(f'Model: {bot.model}' f' | Temp: {bot.temperature}')
    print('Type /help for commands.')
    while True:
        try:
            user_input = input('You: ')
            if user_input.startswith('/'):
                if not bot.handle_command(user_input):
                    break
                continue
            print("ai :",end="")
            bot.chat(user_input)
            print()
        except KeyboardInterrupt:
            print('\nBye!')
            break

    
if __name__ == "__main__":
    main()