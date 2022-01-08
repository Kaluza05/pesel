from random import randint
import names
import pandas as pd
from pandas.core.frame import DataFrame

def pesel():
    global WAGE
    WAGE = [1,3,7,9,1,3,7,9,1,3]
    year = randint(1900,2099)
    month = randint(1,12)
    day31_months = [1,3,5,7,8,10,12]
    day30_months = [4,6,9,11]
    if year>=2000:
        month +=20
        day31_months = [i+20 for i in day31_months]
        day30_months = [i+20 for i in day30_months]
    if month % 20  ==  2: 
        if year % 4 == 0: # sprawdza lata przestepne
            if year % 100 == 0:
                if year % 400 == 0:
                    day_range = 29
                else:
                    day_range = 28
            else:
                day_range = 29
        else:
            day_range = 28
        day = randint(1,day_range)
    elif month in day31_months:
        day = randint(1,31)
    elif month in day30_months:
        day = randint(1,30)
    RR = str(year)[-2:] 
    MM = str(month).zfill(2)
    DD = str(day).zfill(2)
    PPPP = ''.join([str(randint(0,9)) for _ in range(4)])
    K = str(10 - int(str(sum([int(str(int(i)*wage)[-1]) for i,wage in zip(list(RR+MM+DD+PPPP),WAGE)]))[-1]))[-1]
    return RR+MM+DD+PPPP+K

def validate_pesel(pesel): #sprawdza czy liczba kontrolna się zgadza
    if pesel[-1] == str(10 - int(str(sum([int(str(int(i)*wage)[-1]) for i,wage in zip(list(pesel[:-1]),WAGE)]))[-1]))[-1]:
        return True
    return False

class NotFound(Exception): #wyjątek który ma być wywołany jeżeli wprowadzony pesel nie zostanie znaleziony
    def __init__(self,spec,value,message = " not found on the list"):
        self.spec = spec
        self.value = value 
        self.message = message
        super().__init__(f'{self.spec}{self.message}: "{self.value}"')
class WrongPesel(Exception): #wyjątek który ma byc wywołany jeżeli liczba kontrolna wprowadzonego peselu sie nie zgadza
    def __init__(self, pesel,*,message = "Pesel that you provided doesn't exist or got repeated"):
        self.pesel = pesel 
        self.message = message
        super().__init__(f'{self.message}: "{self.pesel}"')

class Society: # tworzenie zbiorowiska obywateli 
    def __init__(self,population):
        self.population = population
        self.citizens = { index : Citizen()  for index in range(1,population+1)} #słownik z indexem oraz 'adresem' klasy Citizen
        self.society_dt = pd.DataFrame({
         'indieces': self.citizens.keys(),
         'name': [person.get_name() for person in self.citizens.values()],
         'pesel': [person.get_pesel() for person in self.citizens.values()],
         'gender' : [person.gender() for person in self.citizens.values()]})
    def __repr__(self): #wyświetla imię obywatela oraz jego pesel i index
        return self.society_dt.to_string(index= False)
    def society_dataframe(self):
        return self.society_dt
    def add_citizen(self): # dodaje nowego obywatela z losowo wygenerowanym peselem
        self.new_citizen = Citizen()
        self.new_dataframe = pd.DataFrame({ 
         'indieces': self.population +1 ,
         'name': [self.new_citizen.get_name()],
         'pesel': [self.new_citizen.get_pesel()],
         'gender' : [self.new_citizen.gender()] })
        if self.new_dataframe['pesel'].to_string(index=False) not in self.society_dt['pesel'].tolist():
            self.society_dt =  self.society_dt.append(self.new_dataframe,ignore_index=True)
            self.population +=1
        else: raise WrongPesel(self.new_dataframe['pesel'].to_string(index = False),message ='Pesel got repeated') #wywołuje błąd jeśli pesel juz istnieje
        
    def ban_citizen(self,citizens_index): #usuwa obywatela ze społeczeństwa
        if citizens_index in self.society_dt['indieces'].tolist():
            self.population -= 1
            self.society_dt = self.society_dt[self.society_dt['indieces'] != citizens_index].reset_index(drop=True)
            self.society_dt['indieces'] = [i for i in range(1,self.count_population()+1)]
        else: raise NotFound("Index",citizens_index)

    def change_pesel(self,index,new_pesel): # podmienia stary pesel obywatela z nowo podanym
        if len(new_pesel) <= 11 and validate_pesel(new_pesel) and new_pesel not in self.society_dt["pesel"].tolist():
            if index in self.society_dt['indieces'].tolist():
                self.society_dt.at[index-1,'pesel'] = new_pesel
            else: raise NotFound("Index",index)
        else: raise WrongPesel(new_pesel)

    def get_info(self,index):
        return self.society_dt.drop("indieces",axis=1).loc[index-1].to_string()
    def count_woman(self): # liczy ile jest kobiet w społeczeństwie
        return self.society_dt['gender'].tolist().count('female')
    def count_man(self): # liczy ile jest mężczyzn w społeczeństwie
        return self.society_dt['gender'].tolist().count('male')
    def count_population(self): #populacja społeczeństwa
        return self.population

class Citizen: # tworzenie każdego obywatela, przypisanie pesela oraz imienia
    def __init__(self):
        self.pesel = pesel()
        self.name = names.get_full_name(gender= self.gender())
    def get_name(self):
        return self.name
    def get_pesel(self):
        return self.pesel
    def gender(self):
        if int(self.pesel[-2]) % 2 == 0:
            return 'female'
        return 'male'
