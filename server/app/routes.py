from flask import jsonify
from app.services import EnergyDataService

energy_service = EnergyDataService()

def init_routes(app):
    @app.route('/')
    def index():
        return jsonify(message="Bem-vindo ao backend do sistema de consumo de energia")

    # @app.route('/energy-data/<string:country>')
    # def get_energy_data(country):
    #     code, renewables, non_renewables = energy_service.get_energy_consumption(country)
    #     if not renewables.empty and not non_renewables.empty:
    #         return jsonify({
    #             'code': code,
    #             'data': {
    #                 'renewables': renewables,
    #                 'non_renewables': non_renewables
    #             }
    #         })
    #     return jsonify({'error': 'País não encontrado'}), 404
    
    @app.route('/predict/<string:country>/<string:energy_type>/<int:years>')
    def predict_future_consumption(country, energy_type, years):
        df = energy_service.energy_model.df
        code, data = energy_service.predict_future_consumption(df, country, energy_type, years)
        if data is not None:
            return jsonify({
                'code': code,
                'data': data
            })
        return jsonify({'error': 'Dados insuficientes para fazer a predição'}), 404
    
    @app.route('/top10_renewable')
    def top10_renewable():
        df = energy_service.energy_model.df
        code, data = energy_service.get_top10_renewable(df)

        if code == 200: 
            return jsonify({
                'code': code,
                'data': data
            })
        
        return jsonify({'message': 'Erro ao buscar dados'}), 500
    
    @app.route('/top10_nonrenewable')
    def top10_nonrenewable():
        df = energy_service.energy_model.df
        code, data = energy_service.get_top10_nonrenewable(df)

        if code == 200: 
            return jsonify({
                'code': code,
                'data': data
            })
        
        return jsonify({'message': 'Erro ao buscar dados'}), 500