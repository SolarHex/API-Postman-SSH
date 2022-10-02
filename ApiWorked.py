from concurrent.futures import thread
from distutils.log import debug
import json
import pandas as pd
from flask import Flask, abort, current_app, request
from flask_restful import Resource, Api,reqparse
from flask import Flask,send_file,send_from_directory

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=["GET","POST"], host="myhost.com")
def process_json():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            results = request.json
            # return results
            JsonData = json.dumps(results)
            with open('JsonData.json', 'w', encoding='utf-8') as f:
                info = f.write(JsonData)
            with open('JsonData.json', 'r', encoding='utf-8') as outsourse:
                info = json.load(outsourse)
                estimate = info["data"][0]
                    
                chapter_one = pd.Series({
                        'пользователь':info['ward'],
                        'Время заполнения анкеты':estimate['fill_date'],
                        'Стадия заболевания':estimate['ward.data.mank_ill_stage'],
                        'Дата заполнения':'?',
                        'Мед.анкета подтвержена':'?',
                        "":"",
                        """Блок 1 | Общая информация о пациенте и заболевании (Блок появляется для всех пользователей любого возраста) (Блок появляется только в первичной анкете)""":'',
                        """Возраст постановки диагноза миодистрофия Дюшенна/Беккера""":info["ward.data.mank_diagnosis_age_2"],
                        """Возраст постановки диагноза миодистрофия Дюшенна/Беккера""":'?',
                        """Где впервые заподозрили(предположили) диагноз миодистрофия Дюшенна/Беккера?
                        Вам необходимо выбрать учреждение из списка. Если перечисленные варианты Вам не подходят - указжите только свой ответ""" :info['ward.data.mank_first_place_2'],
                        """Где проводилось генетическое исследование и подтвердился диагноз""":info['ward.data.mank_gen_research_place_2'],
                        'Какая мутация выявлена?':info['ward.data.mank_mutation_detected_2'],
                        'Отметьте конкретный участок гена, где произошла мутация':info["ward.data.mank_gen_select"],
                        'Дополнительная поломка':'?',
                        'Есть ли среди ваших родственников случаи заболевания миодистрофией Дюшенна/Беккера?':info["ward.data.mank_family_illness_2"],
                        'Является ли мама ребенка носительницей мутации?':info['ward.data.mank_mother_carrier_2'],
                        'Есть ли еще в вашей семье дети с миодистрофией Дюшенна?':info['ward.data.mank_kids_illness_2'],
                        """Сопутствующие диагнозы. Если у ребенка диагностированы другие заболевания кроме миодистрофии Дюшенна/Беккера, выберите их все в данном пункте""":info['ward.data.mank_accompanying_diagnosis_2'],
                        'Блок 2| Неврология (открыт всем) (1р/год)':'',
                        'Сколько раз за последний год вы были на приеме у невролога?':estimate['ward.data.mank_neuro_last_visit_2'],
                        """Укажите вес ребенка в кг (важно, чтобы данные были актуальными на момент заполнения)""":estimate['ward.data.mank_weight_2'],
                        """Укажите рост ребенка в см (важно, чтобы данные были актуальными на момент заполнения)""":estimate['ward.data.mank_height_2'],
                        'Какие двигательные возможности у сына на данный момент?':estimate['ward.data.mank_motor_abilities_2'],
                        'В каком возрасте ваш сын потерял способность самостоятельной ходьбы?':estimate['ward.data.mank_neuro_lost_ability'],
                        'Получает ли ребенок стероидную терапию (преднизолон/дефлазакорт)?':estimate['ward.data.mank_neuro_steroids_2'],
                        'Укажите схему приема и дозировку':estimate['ward.data.mank_neuro_steroids_treatment_2'],
                        'С какого возраста начали стероидную терапию?':estimate['ward.data.mank_neuro_treatment_start_age_2'],
                        'Наблюдаются ли побочные эффекты от стероидной терапии?':estimate['ward.data.mank_neuro_treatment_side_effects_2'],
                        'Есть ли у вас опыт иной (генной или клеточной) терапии?':estimate['ward.data.mank_neuro_gen_therapy'],
                        'Укажите, пожалуйста, вид применяемой терапии':estimate['ward.data.mank_neuro_gen_therapy_type'],
                        'Когда вы начали применение такой терапии? Укажите месяц и год':estimate['ward.data.mank_neuro_gen_therapy_start'],
                        'Проводилось ли исследование мышечной силы ребенку? ':estimate['ward.data.mank_neuro_muscle_study_2'],
                        'Укажите балл мышечной силы рук при его наличии ':estimate['ward.data.mank_neuro_muscle_study_ball'],
                        'Ребенок говорит о наличии у него болезненных ощущений? Если да, то о каких':estimate['ward.data.mank_pain_symptoms_2'],
                        'Блок 3| Ортопедия (открыт всем, кроме Пресимптоматической стадии) (2р/год)':'',
                        'Сколько раз за последний год вы были на приеме у ортопеда?':estimate['ward.data.mank_orotho_last_visit_2'],
                        'Проводилась ли рентгенография грудного и поясничного отдела позвоночников в боковой проекции за последний год?':estimate['ward.data.mank_orotho_xray_chest_2'],
                        'Есть ли у ребенка сколиоз?':estimate['ward.data.mank_orotho_scoliosis_2'],
                        'Укажите степень и угол сколиоза при наличии (обычно указывается в выписке от ортопеда)':estimate['ward.data.mank_orotho_scoliosis_details_2'],
                        'Ребёнок используете корсет?':estimate['ward.data.mank_orothoscoliosis_corset_2'],
                        'Есть ли у вашего сына контрактуры (состояние, при котором конечность не может быть полностью согнута или разогнута)?':estimate['ward.data.mank_orotho_contracture_2'],
                        'Перечислите, в каких именно местах контрактуры сформировались/ухудшились за последний год':estimate['ward.data.mank_orotho_contracture_details_2'],
                        'Вы используете ортезы/тутора на голени/на кисти?':estimate['ward.data.mank_orotho_orthosis_2'],
                        'Блок 4| Реабилитация (открыт всем) (2р/год)':'',
                        "Сколько раз ребенок был консультирован физическим терапевтом (вопросы ТСР и физических упражнений\растяжек) за последний год?":estimate['ward.data.mank_rehab_consult'],
                        'Делаете ли вы с ребенком профилактические растяжки?':estimate['ward.data.mank_rehab_stretching'],
                        'Какие технические средства реабилитации (ТСР) рекомендованы сыну?  ':estimate['ward.data.mank_rehab_devices'],
                        'Какими средствами технической реабилитации (ТСР) пользуется ваш сын? ':estimate['ward.data.mank_rehab_devices_used'],
                        'Блок 5|Эндокринология (открыт для всех стадий) (2р\год)':'',
                        'Сколько раз за последний год вы были на приеме у эндокринолога? ':estimate['ward.data.mank_endo_last_visit_2'],
                        'Проводилась ли ребенку денситометрия (диагностика плотности костной ткани) за последний год?':estimate['ward.data.mank_endo_densio_2'],
                        'Напишите результат денситометрии':estimate['ward.data.mank_endo_densio_result_2'],
                        'Проводилась ли вашему сыну оценка полового развития за последний год? ':estimate['ward.data.mank_endo_pubert_test_2'],
                        'Соответсвует половое развитие возрастной норме?':estimate['ward.data.mank_endo_pubert_test_result_2'],
                        'Проводилось ли измерение роста':estimate['ward.data.mank_endo_height_measure'],
                        'Блок 6| Пульмонология (Стадия 2 поздняя амбулаторная 1р\год (проведение исследования ФВД, научение пользованию). Стадия 3 и 4, мин. 2р/год)':'',
                        'Сколько раз за последний год вы были на приеме у пульмонолога?':estimate['ward.data.mank_pulmo_last_visit_2'],
                        'Сопровождает ли ребенка специалист по респираторной поддержке на регулярной основе? Выберите подходящие варианты. Обычно это пульмонолог или врач-реаниматолог, но у вас может оказаться свой вариант ответа':estimate['ward.data.mank_pulmo_specialist_2'],
                        'За последний год вы проходили исследование функции внешнего дыхания (ФВД)?':estimate['ward.data.mank_pulmo_breath_res_last_2'],
                        'Введите показатели ФЖЕЛ (форсированная жизненная емкость легких) в процентах, если есть информация за текущий год':estimate['ward.data.mank_pulmo_breath_res_FJEL_2'],
                        'Введите показатели ЖЕЛ (жизненная емкость легких) в процентах, если есть информация за текущий год ':estimate['ward.data.mank_pulmo_breath_res_JEL_2'],
                        'Ведители показатели — ПСК (пиковая скорость кашля) л/мин, если есть информация за текущий год':estimate['ward.data.mank_pulmo_breath_res_PKS_2'],
                        'Проводилось ребенку исследование сна (полисомнография, кардиомониторинг, ночная пульсоксометрия и под.)':estimate['ward.data.mank_pulmo_breath_dream_research'],
                        'Наблюдалось ли падение сатурации ниже 95% , если есть информация за прошедший год?':estimate['ward.data.mank_pulmo_saturation'],
                        'Жалуется ли ваш ребенок на (отметьте нужное)':estimate['ward.data.mank_pulmo_symptoms_2'],
                        'Какие медицинские приборы вы используете?':estimate['ward.data.mank_pulmo_med_devices_2'],
                        'Делаете ли вы дыхательную гимнастику с сыном?':estimate['ward.data.mank_pulmo_gym'],
                        'Как именно делаете дыхательную гимнастику?':estimate['ward.data.mank_pulmo_gym_fact'],
                        'Использует ли ваш сын аппарат вентиляции легких?':estimate['ward.data.mank_pulmo_nivl_2'],
                        'Сколько часов вентиляции требуется вашему сыну?':estimate['ward.data.mank_pulmo_nivl_time'],
                        'Может ли сын быть на спонтанном дыхании (когда аппарат выключен)?':estimate['ward.data.mank_pulmo_breath_ability'],
                        'Блок 7| Гастроэнтерология (для всех стадий) (2р в год)':'',
                        'Сколько раз за последний год вы были на приеме у гастроэнтеролога?':estimate['ward.data.mank_gastro_last_visit_2'],
                        'Отметьте (если есть жалобы на) гастроэнтерологические проблемы ребенка?':estimate['ward.data.mank_gastro_symptoms_2'],
                        'Как питается сын в настоящий момент?':estimate["ward.data.mank_gastro_current_diet_2"],
                        'Наблюдается потеря веса за последний год?':estimate["ward.data.mank_gastro_weight_loss_2"],
                        'Увеличилось ли время приема пищи?':estimate['ward.data.mank_gastro_dinner_time_2'],
                        'Проводилось ли УЗИ органов брюшной полости за последний год?':estimate['ward.data.mank_gastro_uzi'],
                        'Блок 8| Кардиология (Пре и Стадия 1 - 1р\год, Стадия 2 -мин.1р\год. Стадия 3-4 2р\год или чаще)':'',
                        'Сколько раз за последний год вы были на приеме у кардиолога?':estimate['ward.data.mank_cardio_last_visit_2'],
                        'Получает ли ребенок кардиологическую терапию сейчас? ':estimate['ward.data.mank_cardio_mrt_2'],
                        'Если сын получал кардиологическую терапию раньше, а сейчас она отменена, укажите, пожалуйста, причину':estimate['ward.data.mank_cardio_therapy_2'],
                        'За последний год проводилось УЗИ сердца (Эхо-КГ)?':estimate['ward.data.mank_cardio_therapy_cancel'],
                        'За последний год проводилось ЭКГ сердца?':estimate['ward.data.mank_cardio_uzi_2'],
                        'За последний год проводилось МРТ сердца?':estimate["ward.data.mank_cardio_ekg"],
                        'Блок 9|Хирургические вмешательства (для всех стадий) (1р/год)':'',
                        'Были ли у ребенка операции за последний год?':estimate["ward.data.mank_surgery_state_2"],
                        'По какому поводу проводилось хирургическое вмешательство?':estimate['ward.data.mank_surgery_state_fact_2'],
                        'Блок 10| Социальный/Возможности среды (для всех стадий) (1р/год)':'',
                        "Форма обучения":estimate['ward.data.mank_social_adapt_2'],
                        'Насколько часто получется у вашего сына общаться со сверстниками?':estimate['ward.data.mank_social_connection_2'],
                        'Приспособлено ли место, где вы живете (квартира, дом)  для людей с инвалидностью ?':estimate['ward.data.mank_social_studyform_2'],
                        'Блок 11| Социально–психологический блок (для всех стадий) (1р/год)':'',
                        'Как вы оцениваете психологическое состояние сына?':estimate["ward.data.mank_psy_state_2"],
                        'Получает ли сын поддержку психолога в настоящий момент? ':estimate['ward.data.mank_psy_support_2'],
                        'Получаете ли вы поддержку от психолога/психотерапевта?':estimate["ward.data.mank_psy_personal_support_2"]
                    })
                    
                conclution = pd.DataFrame({
                        """К каждому блоку (кроме Блока 1) в начале идет примечание Обратите, пожалуйста, внимание: информацию по блоку «...» вы заполняете за текущий календарный год.""":chapter_one
                    })
                    
                writer = pd.ExcelWriter("CompanyElmaResult.xlsx")
                conclution.to_excel(writer,"Company")
                writer.save()
                return info, 200
        else:
            return "He had a dream ASAP to die !"
    except FileNotFoundError:
        abort(404)

@app.route('/',methods = ['GET','POST'], host="mymiofond.com/get-csv/CompanyElmaResult.xlsx")
def get_csv(csv_filename="CompanyElmaResult.xlsx"):
    try:
        return send_file(csv_filename,as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/',methods = ['GET','POST'], host="mymiofond.com/getting")
def method():
    try:
        return {"project":"http://127.0.0.1:1488/get-csv/CompanyElmaResult.xlsx"}
    except FileNotFoundError:
        return "PZDC"
    
if __name__ == "__main__":
    #app.run(host='0.0.0.0',port = 8000, threaded = True, debug = True)
    # app.run(host = '/mymiofond.ru', debug = True, threaded = True)
    website_url = 'mymiofond.com:5000'
    app.config['SERVER_NAME'] = website_url
    app.run()