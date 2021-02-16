from dataclasses import dataclass

@dataclass
class Constitution:
    # Constitucion Politica de Colombia
    name: str
    # Colombia
    country: str
    # creacion 1991
    year: int
    # Ultima actualizacion: 2016
    last_update: int
    ''' url para consulta externa:
    https://www.procuraduria.gov.co/iemp/media/file/ejecucion/
    Constituci%C3%B3n%20Pol%C3%ADtica%20de%20Colombia%202020.pdf'''
    url: str

    ''' Map of titles
    title 1: N caps, x arts.
    '''

    def get_articles(self, text):
        pass

Colombiana = Constitution(
    name = 'Constitucion Politica de Colombia',
    country = 'Colombia',
    year = 1991,
    last_update = 2016,
    # We must use a bit.ly to record the traffic that we send
    url = 'https://www.procuraduria.gov.co/iemp/media/file/ejecucion/Constituci%C3%B3n%20Pol%C3%ADtica%20de%20Colombia%202020.pdf'
)