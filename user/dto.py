from dataclasses import dataclass

@dataclass
class SignupDto():
  email:str
  nickname:str
  password:str