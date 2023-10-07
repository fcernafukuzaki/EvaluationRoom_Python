import pandas as pd
from configs.resources import db, text
from configs.logging import logger
# from objects.selectionprocess import SelectionProcess, SelectionProcessSchema
# from objects.selectionprocess_info import SelectionProcessInfo, SelectionProcessInfoSchema, SelectionProcessInfoResumenSchema, CandidatePsychologicalTestInfoSchema, CandidateWithoutSelectionProcessSchema, CandidatePsychologicalTestWithoutSelectionProcessInfoSchema

# selectionprocess_schema = SelectionProcessSchema()
# selectionprocesses_info_schema = SelectionProcessInfoSchema(many=True)
# candidates_psychologicaltest_info_schema = CandidatePsychologicalTestInfoSchema(many=True)
# selection_process_info_resumen_schema = SelectionProcessInfoResumenSchema(many=True)
# candidates_without_selection_process_info_resumen_schema = CandidateWithoutSelectionProcessSchema(many=True)
# candidates_psychologicaltest_without_selection_process_info_schema = CandidatePsychologicalTestWithoutSelectionProcessInfoSchema(many=True)

class SelectionProcessService():
    """
    Obtener datos relacionados a los procesos de selección.
    """

    # def get_selectionprocesses(self, idclient, idjobposition, processStatus):        
    #     if idclient and idjobposition:
    #         all_selectionprocess = SelectionProcess.query.get((idclient, idjobposition))
    #     elif idclient and not idjobposition:
    #         all_selectionprocess = SelectionProcess.query.filter(SelectionProcess.idclient==idclient).all()
    #     elif not idclient and idjobposition:
    #         return {'message': 'Client identity is required'}, 500
    #     else:
    #         resumen_selectionprocess = SelectionProcessInfo.resumen
    #         all_selectionprocess = SelectionProcessInfo.selectionprocess_info(processStatus)
    #         all_candidates_psychologicaltes = SelectionProcessInfo.candidates_psychologicaltest_info(processStatus)
        
    #     if all_selectionprocess and idclient and idjobposition:
    #         result = selectionprocess_schema.jsonify(all_selectionprocess)
    #         return result
    #     else:
    #         result = selection_process_info_resumen_schema.dump(resumen_selectionprocess),selectionprocesses_info_schema.dump(all_selectionprocess),candidates_psychologicaltest_info_schema.dump(all_candidates_psychologicaltes)
    #         return jsonify(result)
    #     return {'message': 'Not found'}, 404

    def format_date(self, value):
        if pd.notna(value):
            return value.strftime('%Y-%m-%d')
        else:
            return None

    
    def get_candidates_without_selectionprocess(self, correoelectronico):
        """
        Obtener la lista de candidatos que no están asignados a un proceso de selección.
        """
        result = None
        try:
            sql_query = f"""
            SELECT c.idcandidato, c.nombre, c.apellidopaterno, c.apellidomaterno,
                c.nombre || ' ' || c.apellidopaterno || ' ' || c.apellidomaterno AS "nombre_completo",
                c.fechanacimiento, c.fecharegistro AT TIME ZONE 'America/Lima' AS "fecha_registro", c.correoelectronico,
                c.selfregistration,
                (SELECT tel.numero FROM evaluationroom.candidatotelefono tel WHERE tel.idtelefono=1 AND tel.idcandidato=c.idcandidato) AS "telefono_movil",
                (SELECT tel.numero FROM evaluationroom.candidatotelefono tel WHERE tel.idtelefono=2 AND tel.idcandidato=c.idcandidato) AS "telefono_fijo",
                (SELECT COUNT(ctest.idcandidato) 
                    FROM evaluationroom.candidatotest ctest
                    WHERE ctest.idcandidato=c.idcandidato) AS "cant_examenes_asignados",
                (SELECT COUNT(ctest.idcandidato) 
                    FROM evaluationroom.candidatotest ctest
                    WHERE ctest.idcandidato=c.idcandidato
                    AND ctest.fechaexamen IS NOT NULL
                ) AS "tiene_resultado",
                u.idusuario, u.nombre AS "usuario_nombre", u.correoelectronico AS "usuario_correoelectronico", 
                u.idempresa, up.idperfil, pe.nombre AS "perfil_nombre", 
                e.nombre AS "empresa_nombre", e.activo AS "empresa_activo", 
                cli.idcliente, cli.nombre AS "cliente_nombre",
                pl.idpuestolaboral, pl.nombre AS "puestolaboral_nombre",
                sp.fecha_inicio_proceso, sp.fecha_fin_proceso, sp.usuario_registro, sp.activo AS "procesoseleccion_activo",
                (SELECT COUNT(spc.idcandidato) FROM evaluationroom.procesoseleccioncandidato spc WHERE spc.idempresa=sp.idempresa AND spc.idcliente=sp.idcliente AND spc.idpuestolaboral=sp.idpuestolaboral) AS "cantidad_candidatos",
                c_test.idtestpsicologico,
				testp.nombre AS "nombre_test",
				c_test.fechaexamen AT TIME ZONE 'America/Lima' AS "fechaexamen",
				testp.cantidadpreguntas AS "cantidad_preguntas_test",
                (SELECT COUNT(ctestdet.idcandidato) 
                    FROM evaluationroom.candidatotestdetalle ctestdet
                    WHERE ctestdet.idcandidato=c.idcandidato AND ctestdet.idtestpsicologico=c_test.idtestpsicologico
				) AS "cantidad_preguntas_respondidas",
                (SELECT CASE WHEN COUNT(ctest.idcandidato) = 1 THEN TRUE ELSE FALSE END CASE
                    FROM evaluationroom.candidatotest ctest
                    WHERE ctest.idcandidato=c.idcandidato
                    AND ctest.idtestpsicologico=c_test.idtestpsicologico
                    AND ctest.resultado IS NOT NULL
                ) AS "tiene_resultado_test"
            FROM evaluationroom.usuario u
            INNER JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario
            INNER JOIN evaluationroom.perfil pe ON up.idperfil=pe.idperfil
            INNER JOIN evaluationroom.empresa e ON u.idempresa=e.idempresa
            INNER JOIN evaluationroom.cliente_ cli ON u.idempresa=cli.idempresa
            INNER JOIN evaluationroom.puestolaboral_ pl ON pl.idempresa=cli.idempresa AND pl.idcliente=cli.idcliente
            INNER JOIN evaluationroom.procesoseleccion sp ON sp.idempresa=pl.idempresa AND sp.idcliente=pl.idcliente AND sp.idpuestolaboral=pl.idpuestolaboral
            INNER JOIN evaluationroom.procesoseleccioncandidato spc ON spc.idempresa=sp.idempresa AND spc.idcliente=sp.idcliente AND spc.idpuestolaboral=sp.idpuestolaboral
            INNER JOIN evaluationroom.candidato c ON c.idcandidato=spc.idcandidato
            LEFT JOIN evaluationroom.candidatotest c_test ON c_test.idcandidato=c.idcandidato
            LEFT JOIN evaluationroom.testpsicologico testp ON testp.idtestpsicologico=c_test.idtestpsicologico
            WHERE u.activo=true
            AND up.idperfil IN (2, 3)
            AND u.correoelectronico='{correoelectronico}'
            GROUP BY c.idcandidato, 
                u.idusuario, u.nombre, u.correoelectronico, u.idempresa, up.idperfil, pe.nombre, 
                e.nombre, e.activo, cli.idcliente, cli.nombre,
                pl.idpuestolaboral, pl.nombre,
                sp.idempresa, sp.idcliente, sp.idpuestolaboral, sp.fecha_inicio_proceso, sp.fecha_fin_proceso, sp.usuario_registro, sp.activo,
                c_test.idtestpsicologico, testp.nombre, c_test.fechaexamen, testp.cantidadpreguntas
            ORDER BY e.nombre, pe.nombre, u.correoelectronico, cli.nombre, pl.nombre, c.idcandidato DESC, c_test.idtestpsicologico ASC
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            procesos = db.execute(text(sql_query))

            # Obtén los resultados del cursor como una lista de diccionarios
            results = procesos.fetchall()

            # Convierte los resultados a un DataFrame de pandas
            df_results = pd.DataFrame(results)
            
            # Resultado en formato de lista
            data = []

            campos = ["idusuario", "usuario_nombre", "usuario_correoelectronico", "idempresa", "empresa_nombre", "empresa_activo", "idperfil", "perfil_nombre"]
            df = df_results[campos].copy()
            unique_usuario = df[campos].drop_duplicates()
            # Convierte el DataFrame a un diccionario
            unique_usuario = unique_usuario.to_dict(orient="records")

            campos = ["idempresa", "idcliente", "cliente_nombre"]
            df_empresas = df_results[campos].copy()
            unique_empresas = df_empresas[campos].drop_duplicates()
            
            campos = ["idempresa", "idcliente", "idpuestolaboral", "puestolaboral_nombre", "fecha_inicio_proceso", "fecha_fin_proceso", "usuario_registro", "procesoseleccion_activo", "cantidad_candidatos"]
            df_procesosseleccion = df_results[campos].copy()
            unique_procesosseleccion = df_procesosseleccion[campos].drop_duplicates()
            unique_procesosseleccion["fecha_inicio_proceso"] = unique_procesosseleccion["fecha_inicio_proceso"].apply(self.format_date)
            unique_procesosseleccion["fecha_fin_proceso"] = unique_procesosseleccion["fecha_fin_proceso"].apply(self.format_date)

            campos = ["idempresa", "idcliente", "idpuestolaboral", "idcandidato", "nombre", "apellidopaterno", "apellidomaterno", "nombre_completo", "fechanacimiento", "fecha_registro", "correoelectronico", "selfregistration", "telefono_movil", "telefono_fijo", "cant_examenes_asignados", "tiene_resultado"]
            unique_candidatos = df_results[campos].copy()
            unique_candidatos = unique_candidatos[campos].drop_duplicates()
            unique_candidatos["fechanacimiento"] = unique_candidatos["fechanacimiento"].dt.strftime('%Y-%m-%d').astype(str).replace("nan", None)
            unique_candidatos["fecha_registro"] = unique_candidatos["fecha_registro"].dt.strftime('%Y-%m-%d %H:%M:%S').astype(str).replace("nan", None)

            campos = ["idcandidato", "idtestpsicologico", "nombre_test", "fechaexamen", "cantidad_preguntas_test", "cantidad_preguntas_respondidas", "tiene_resultado_test"]
            unique_testpsicologicos = df_results[campos].copy()
            unique_testpsicologicos["fechaexamen"] = unique_testpsicologicos["fechaexamen"].dt.strftime('%Y-%m-%d %H:%M:%S').astype(str).replace("nan", None)

            for row in unique_usuario:
                data_proceso = dict()
                data_proceso["usuario"] = {
                    "idusuario": row.get("idusuario"),
                    "nombre": row.get("usuario_nombre"),
                    "correoelectronico": row.get("usuario_correoelectronico"),
                    "perfil": {
                        "idperfil": row.get("idperfil"), 
                        "nombre": row.get("perfil_nombre"),
                    }
                }
                
                data_proceso["empresa"] = {
                    "idempresa": row.get("idempresa"),
                    "nombre": row.get("empresa_nombre"),
                    "activo": row.get("empresa_activo"),
                }
                
                filtro = unique_empresas['idempresa'] == row.get("idempresa")
                empresas = unique_empresas[filtro]
                empresas = empresas.to_dict(orient="records")
                data_empresas = []
                for row_empresa in empresas:
                    data_empresa = {
                        "idcliente": row_empresa.get("idcliente"),
                        "nombre": row_empresa.get("cliente_nombre")
                    }

                    filtro = ((unique_procesosseleccion['idempresa'] == row_empresa.get("idempresa")) & (unique_procesosseleccion['idcliente'] == row_empresa.get("idcliente")))
                    procesosseleccion = unique_procesosseleccion[filtro]
                    procesosseleccion = procesosseleccion.to_dict(orient="records")
                    data_procesosseleccion = []
                    for row_procesoseleccion in procesosseleccion:
                        data_procesoseleccion = {
                            "idpuestolaboral": row_procesoseleccion.get("idpuestolaboral"),
                            "nombre": row_procesoseleccion.get("puestolaboral_nombre"),
                            "fecha_inicio_proceso": row_procesoseleccion.get("fecha_inicio_proceso"),
                            "fecha_fin_proceso": row_procesoseleccion.get("fecha_fin_proceso"),
                            "usuario_registro": row_procesoseleccion.get("usuario_registro"),
                            "activo": row_procesoseleccion.get("procesoseleccion_activo"),
                            "cantidad_candidatos": row_procesoseleccion.get("cantidad_candidatos")
                        }
                        
                        filtro = ((unique_candidatos['idempresa'] == row_procesoseleccion.get("idempresa")) & 
                                  (unique_candidatos['idcliente'] == row_procesoseleccion.get("idcliente")) & 
                                  (unique_candidatos['idpuestolaboral'] == row_procesoseleccion.get("idpuestolaboral")))
                        candidatos = unique_candidatos[filtro]
                        candidatos = candidatos.to_dict(orient="records")
                        data_candidatos = []
                        for row_candidato in candidatos:
                            data_candidato = {
                                "idcandidato": row_candidato.get("idcandidato"),
                                "nombre": row_candidato.get("nombre"),
                                "apellidopaterno": row_candidato.get("apellidopaterno"),
                                "apellidomaterno": row_candidato.get("apellidomaterno"),
                                "nombre_completo": row_candidato.get("nombre_completo"),
                                "fechanacimiento": row_candidato.get("fechanacimiento"),
                                "fecha_registro": row_candidato.get("fecha_registro"),
                                "correoelectronico": row_candidato.get("correoelectronico"),
                                "selfregistration": row_candidato.get("selfregistration"),
                                "telefono_movil": row_candidato.get("telefono_movil"),
                                "telefono_fijo": row_candidato.get("telefono_fijo"),
                                "cant_examenes_asignados": row_candidato.get("cant_examenes_asignados"),
                                "tiene_resultado": row_candidato.get("tiene_resultado")
                            }
                            
                            # filtro = ((unique_testpsicologicos['idcandidato'] == row_candidato.get("idcandidato")))
                            # testpsicologicos = unique_testpsicologicos[filtro]
                            # testpsicologicos = testpsicologicos.to_dict(orient="records")
                            testpsicologicos = unique_testpsicologicos.query(f"idcandidato == {row_candidato['idcandidato']}").to_dict(orient="records")

                            data_candidato['testpsicologicos'] = [
                                {
                                    'idcandidato': row_testpsicologico.get("idcandidato"),
                                    'idtestpsicologico': row_testpsicologico.get("idtestpsicologico"),
                                    'nombre': row_testpsicologico.get("nombre_test"),
                                    'fechaexamen': row_testpsicologico.get("fechaexamen"),
                                    'cantidad_preguntas_test': row_testpsicologico.get("cantidad_preguntas_test"),
                                    'cantidad_preguntas_respondidas': row_testpsicologico.get("cantidad_preguntas_respondidas"),
                                    'tiene_resultado': row_testpsicologico.get("tiene_resultado_test")
                                }
                                for row_testpsicologico in testpsicologicos
                                if row_testpsicologico.get('nombre_test') is not None
                            ]
                            
                            data_candidatos.append(data_candidato)
                        data_procesoseleccion["candidatos"] = data_candidatos
                        data_procesosseleccion.append(data_procesoseleccion)

                    data_empresa["procesosseleccion"] = data_procesosseleccion
                    data_empresas.append(data_empresa)
                
                data_proceso['clientes'] = data_empresas
                data.append(data_proceso)
                
            if int(procesos.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró procesos de selección.'
            else:
                code, message = 404, 'No existen procesos de selección.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los procesos de selección en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message


    # def add_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
    #     process_active = str2bool(process_active)

    #     new_selectionprocess = SelectionProcess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
    #     db.session.add(new_selectionprocess)
    #     db.session.commit()
    #     return selectionprocess_schema.jsonify(new_selectionprocess)
    
    # def update_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
    #     selectionprocess = SelectionProcess.query.get((idclient, idjobposition))

    #     if selectionprocess:
    #         process_active = str2bool(process_active)

    #         selectionprocess.date_process_begin = date_process_begin
    #         selectionprocess.date_process_end = date_process_end
    #         selectionprocess.user_register = user_register
    #         selectionprocess.process_active = process_active
    #     else:
    #         selectionprocess = self.add_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
            
    #     db.session.commit()
    #     return selectionprocess_schema.jsonify(selectionprocess)

    # def delete_selectionprocess(self, idclient, idjobposition):
    #     selectionprocess = SelectionProcess.query.get((idclient, idjobposition))

    #     db.session.delete(selectionprocess)
    #     db.session.commit()

    #     return selectionprocess_schema.jsonify(selectionprocess)
