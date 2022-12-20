import numpy as np
from icecream import ic

BREAK = '\n\n------------------------------------------------'

# ============================================================================ #

class CaseWizard:
     
    def __init__(self,
                 input_string: str,
                 from_case: str,
                 to_case: str):
        
        self.input_string = self.preprocess(input_string)
        self.from_case = from_case
        self.to_case = to_case

# ============================================================================ #

    @staticmethod
    def preprocess(input_string: str) -> str:
        val = str(input_string)
        val = val.replace('__', '_')
        val = val.strip()
        return val
    
    @staticmethod
    def valid_case(case: str) -> bool:
        VALID_CASES = [
            'camelCase',
            'snake_case',
            'PascalCase',
            'kebab-case',
            'SCREAMING_SNAKE_CASE'
        ]
        valid = True if case in VALID_CASES else False
        return valid
    
# ============================================================================ #

    def camel_to_snake(self) -> str:
        return self.input_string    # TODO
    
    def camel_to_pascal(self) -> str:
        return self.input_string    # TODO
    
    def camel_to_kebab(self) -> str:
        return self.input_string    # TODO
    
    def camel_to_screaming_snake(self) -> str:
        return self.input_string    # TODO

# ============================================================================ #

    def snake_to_camel(self) -> str:
        val = self.input_string.lower()
        val = val.replace('_', ' ')
        val = val.title()
        val = val.replace(' ', '')
        val = f'{val[0].lower()}{val[1:]}'
        return val
    
    def snake_to_pascal(self) -> str:
        val = self.input_string.lower()
        val = val.replace('_', ' ')
        val = val.title()
        val = val.replace(' ', '')
        return val
    
    def snake_to_kebab(self) -> str:
        val = self.input_string.lower()
        val = val.replace('_', '-')
        return val
    
    def snake_to_screaming_snake(self) -> str:
        val = self.input_string.upper()
        return val

# ============================================================================ #
    
    def pascal_to_camel(self) -> str:
        return self.input_string    # TODO
    
    def pascal_to_snake(self) -> str:
        return self.input_string    # TODO
    
    def pascal_to_kebab(self) -> str:
        return self.input_string    # TODO
    
    def pascal_to_screaming_snake(self) -> str:
        return self.input_string    # TODO
    
# ============================================================================ #
    
    def kebab_to_camel(self) -> str:
        return self.input_string    # TODO
    
    def kebab_to_snake(self) -> str:
        val = self.input_string.lower()
        val = val.replace('-', '_')
        return val
    
    def kebab_to_pascal(self) -> str:
        return self.input_string    # TODO
    
    def kebab_to_screaming_snake(self) -> str:
        val = self.input_string.upper()
        val = val.replace('-', '_')
        return val
    
# ============================================================================ #
    
    def screaming_snake_to_camel(self) -> str:
        return self.input_string    # TODO
    
    def screaming_snake_to_snake(self) -> str:
        val = self.input_string.lower()
        return val
    
    def screaming_snake_to_pascal(self) -> str:
        return self.input_string    # TODO
    
    def screaming_snake_to_kebab(self) -> str:
        val = self.input_string.lower()
        val = val.replace('_', '-')
        return val

# ============================================================================ #

    @property
    def input_string(self) -> str:
        return self._input_string

    @input_string.setter
    def input_string(self, val) -> None:
        if ' ' in val:
            raise ValueError('Input string cannot contain spaces')
        self._input_string = val
        

    @property
    def from_case(self) -> str:
        return self._from_case
    
    @from_case.setter
    def from_case(self, val) -> None:
        if self.valid_case(val):
            self._from_case = val
        else:
            raise ValueError(f'Invalid from_case: {val}.')
        
    @property
    def to_case(self) -> str:
        return self._to_case
    
    @to_case.setter
    def to_case(self, val) -> None:
        if self.valid_case(val):
            self._to_case = val
        else:
            raise ValueError(f'Invalid to_case: {val}.')

# ============================================================================ #

    @classmethod
    def convert(cls,
                input_string: str,
                from_case: str,
                to_case: str) -> str:
        
        wizard = cls(input_string, from_case, to_case)
        
        if wizard.from_case == wizard.to_case:
            print(f'No conversion performed, from_case and to_case are both {wizard.from_case}...')
            return wizard.input_string
        
        switch = f'{wizard.from_case}__{wizard.to_case}'
        
        con = [
            switch == 'camelCase__snake_case',
            switch == 'camelCase__PascalCase',
            switch == 'camelCase__kebab-case',
            switch == 'camelCase__SCREAMING_SNAKE_CASE',
            
            switch == 'snake_case__camelCase',
            switch == 'snake_case__PascalCase',
            switch == 'snake_case__kebab-case',
            switch == 'snake_case__SCREAMING_SNAKE_CASE',
            
            switch == 'PascalCase__camelCase',
            switch == 'PascalCase__snake_case',
            switch == 'PascalCase__kebab-case',
            switch == 'PascalCase__SCREAMING_SNAKE_CASE',
            
            switch == 'kebab-case__camelCase',
            switch == 'kebab-case__snake_case',
            switch == 'kebab-case__PascalCase',
            switch == 'kebab-case__SCREAMING_SNAKE_CASE',
            
            switch == 'SCREAMING_SNAKE_CASE__camelCase',
            switch == 'SCREAMING_SNAKE_CASE__snake_case',
            switch == 'SCREAMING_SNAKE_CASE__PascalCase',
            switch == 'SCREAMING_SNAKE_CASE__kebab-case'
        ]
        
        res = [
            wizard.camel_to_snake(),
            wizard.camel_to_pascal(),
            wizard.camel_to_kebab(),
            wizard.camel_to_screaming_snake(),
            
            wizard.snake_to_camel(),
            wizard.snake_to_pascal(),
            wizard.snake_to_kebab(),
            wizard.snake_to_screaming_snake(),
            
            wizard.pascal_to_camel(),
            wizard.pascal_to_snake(),
            wizard.pascal_to_kebab(),
            wizard.pascal_to_screaming_snake(),
            
            wizard.kebab_to_camel(),
            wizard.kebab_to_snake(),
            wizard.kebab_to_pascal(),
            wizard.kebab_to_screaming_snake(),
            
            wizard.screaming_snake_to_camel(),
            wizard.screaming_snake_to_snake(),
            wizard.screaming_snake_to_pascal(),
            wizard.screaming_snake_to_kebab()
        ]
        
        output_string = np.select(con, res, default='default')
        
        if output_string == 'default':
            raise RuntimeError(f'Something else went wrong...\n'
                               f'Input string: {input_string}\n'
                               f'From case: {wizard.from_case}\n'
                               f'To case: {wizard.to_case}\n')
        else:
            print(f'Converting string from {wizard.from_case} to {wizard.to_case}...\n'
                  f'Input string: {wizard.input_string}\n'
                  f'Output string: {output_string}\n')
            
            return output_string

# ============================================================================ #

if __name__ == '__main__':
    print(f'{BREAK} Executing as standalone script...')
    
    test = 'Blah Blah'
    
    CaseWizard.convert(input_string=test,
                       from_case='PascalCase',
                       to_case='camelCase')