from configs.resources import db
from objects.candidate_form.country import Country, CountrySchema

countries_schema = CountrySchema(many=True)

class CountryService():
    
    def get_countries(self):
        all_countries = Country.query.all()
        if all_countries:
            message = 'Se encontraron registros en base de datos.'
            return countries_schema.dump(all_countries), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message