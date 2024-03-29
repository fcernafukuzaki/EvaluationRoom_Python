from flask import jsonify
from common.util import str2bool
from configs.flask_config import db
from objects.selectionprocess import SelectionProcess, SelectionProcessSchema
from objects.selectionprocess_info import SelectionProcessInfo, SelectionProcessInfoSchema, SelectionProcessInfoResumenSchema, CandidatePsychologicalTestInfoSchema, CandidateWithoutSelectionProcessSchema, CandidatePsychologicalTestWithoutSelectionProcessInfoSchema

selectionprocess_schema = SelectionProcessSchema()
selectionprocesses_info_schema = SelectionProcessInfoSchema(many=True)
candidates_psychologicaltest_info_schema = CandidatePsychologicalTestInfoSchema(many=True)
selection_process_info_resumen_schema = SelectionProcessInfoResumenSchema(many=True)
candidates_without_selection_process_info_resumen_schema = CandidateWithoutSelectionProcessSchema(many=True)
candidates_psychologicaltest_without_selection_process_info_schema = CandidatePsychologicalTestWithoutSelectionProcessInfoSchema(many=True)

class SelectionProcessService():

    def get_selectionprocesses(self, idclient, idjobposition, processStatus):        
        if idclient and idjobposition:
            all_selectionprocess = SelectionProcess.query.get((idclient, idjobposition))
        elif idclient and not idjobposition:
            all_selectionprocess = SelectionProcess.query.filter(SelectionProcess.idclient==idclient).all()
        elif not idclient and idjobposition:
            return {'message': 'Client identity is required'}, 500
        else:
            resumen_selectionprocess = SelectionProcessInfo.resumen
            all_selectionprocess = SelectionProcessInfo.selectionprocess_info(processStatus)
            all_candidates_psychologicaltes = SelectionProcessInfo.candidates_psychologicaltest_info(processStatus)
        
        if all_selectionprocess and idclient and idjobposition:
            result = selectionprocess_schema.jsonify(all_selectionprocess)
            return result
        else:
            result = selection_process_info_resumen_schema.dump(resumen_selectionprocess),selectionprocesses_info_schema.dump(all_selectionprocess),candidates_psychologicaltest_info_schema.dump(all_candidates_psychologicaltes)
            return jsonify(result)
        return {'message': 'Not found'}, 404
    
    def get_candidates_without_selectionprocess(self):        
        all_selectionprocess = SelectionProcessInfo.candidates_without_selectionprocess_info()
        all_candidates_psychologicaltes = SelectionProcessInfo.candidates_psychologicaltest_without_selectionprocess_info()
        
        result = candidates_without_selection_process_info_resumen_schema.dump(all_selectionprocess),candidates_psychologicaltest_without_selection_process_info_schema.dump(all_candidates_psychologicaltes)
        if result:
            return jsonify(result)
        return {'message': 'Not found'}, 404

    def add_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
        process_active = str2bool(process_active)

        new_selectionprocess = SelectionProcess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
        db.session.add(new_selectionprocess)
        db.session.commit()
        return selectionprocess_schema.jsonify(new_selectionprocess)
    
    def update_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
        selectionprocess = SelectionProcess.query.get((idclient, idjobposition))

        if selectionprocess:
            process_active = str2bool(process_active)

            selectionprocess.date_process_begin = date_process_begin
            selectionprocess.date_process_end = date_process_end
            selectionprocess.user_register = user_register
            selectionprocess.process_active = process_active
        else:
            selectionprocess = self.add_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
            
        db.session.commit()
        return selectionprocess_schema.jsonify(selectionprocess)

    def delete_selectionprocess(self, idclient, idjobposition):
        selectionprocess = SelectionProcess.query.get((idclient, idjobposition))

        db.session.delete(selectionprocess)
        db.session.commit()

        return selectionprocess_schema.jsonify(selectionprocess)