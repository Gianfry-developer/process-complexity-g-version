from cProfile import label

import pandas as pd

import Complexity

if __name__ == '__main__':
    # # Carica i dati
    # df_treat = pd.read_csv("C:\\process_mining\\medication_05.csv", encoding='latin1')
    #                        # parse_dates = ['drug_start_date'])
    # df_patient = pd.read_csv("C:\\process_mining\\patient_01.csv", encoding='latin1')
    #                          # parse_dates = ['admission_d_inpat'])
    #
    # # Semplifica i nomi delle colonne per sicurezza
    # df_treat.columns = df_treat.columns.str.lower()
    # df_patient.columns = df_patient.columns.str.lower()
    #
    # # Teniamo solo le colonne necessarie
    # df_treat = df_treat[['patient_id', 'drug_start_date', 'drug_comercial_name']]
    # df_patient = df_patient[['patient_id', 'admission_d_inpat']]
    #
    # df = pd.merge(df_treat, df_patient, on='patient_id', how='left')
    #
    # # Calcola un timestamp assoluto (offset totale in minuti)
    # # df['timestamp'] = df['admission_d_inpat'] + df['drug_start_date']
    # # Convert to Unix timestamp
    #
    # # df['timestamp'] = pd.to_datetime(df['drug_start_date']).astype(int) // 10 ** 9
    #
    # # print(df)
    #
    # df_log = df.rename(columns={
    #     'patient_id': 'case_id',
    #     'drug_comercial_name': 'activity'
    # })[['case_id', 'activity', 'drug_start_date']]
    #
    # # Ordina per case_id e timestamp
    # df_log = df_log.sort_values(by=['case_id', 'drug_start_date'])
    #
    # # Salva il log
    # df_log.to_csv("C:\\process_mining\\event_log_treatment.csv", index=False)
    #

    df_treat = pd.read_csv("/home/ubuntu/data_process_mining/medication_05.csv",
                           encoding='latin1',
                           dtype={'patient_id': str})
    # parse_dates = ['drug_start_date'])
    df_patient = pd.read_csv("/home/ubuntu/data_process_mining/patient_01.csv",
                             encoding='latin1',
                             dtype={'patient_id': str},
                             parse_dates=['admission_date_emerg', 'admission_d_inpat',
                                          'discharge_date', 'icu_date_in']
                             )
    # parse_dates = ['admission_d_inpat'])

    df_diag_er = pd.read_csv('/home/ubuntu/data_process_mining/diagnosis_er_02.csv',
                             encoding='latin1',
                             dtype={'patient_id': str})
    df_diag_hosp = pd.read_csv('/home/ubuntu/data_process_mining/diagnosis_hosp_03.csv',
                               encoding='latin1',
                               dtype={'patient_id': str})
    df_vitals = pd.read_csv('/home/ubuntu/data_process_mining/vital_signs_04.csv',
                            encoding='latin1',
                            dtype={'patient_id': str, 'constants_ing_time': str})
    df_lab = pd.read_csv('/home/ubuntu/data_process_mining/lab_06.csv',
                         encoding='latin1',
                         dtype={'patient_id': str, 'val_result': str, 'result_text': str},
                         low_memory=False)

    admission_events = df_patient[['patient_id', 'admission_date_emerg']].copy()
    admission_events['activity'] = 'ER_ADMISSION'
    admission_events['timestamp'] = admission_events['admission_date_emerg']

    icu_events = df_patient.dropna(subset=['icu_date_in'])[['patient_id', 'icu_date_in']].copy()
    icu_events['activity'] = 'ICU_TRANSFER'
    icu_events['timestamp'] = icu_events['icu_date_in']

    discharge_events = df_patient[['patient_id', 'discharge_date']].copy()
    discharge_events['activity'] = 'DISCHARGE_' + df_patient['destin_discharge']
    discharge_events['timestamp'] = discharge_events['discharge_date']

    er_diag = pd.melt(df_diag_er,
                      id_vars=['patient_id'],
                      value_vars=[col for col in df_diag_er.columns if col.startswith('dia_')],
                      var_name='diag_num',
                      value_name='diagnosis')
    er_diag = er_diag.dropna(subset=['diagnosis'])
    er_diag['activity'] = 'DIAGNOSIS_ER_' + er_diag['diagnosis'].astype(str)  # .str[:50]
    # er_diag['timestamp'] = pd.to_datetime(er_diag['admission_date_emerg'])

    # if 'admission_date_emerg' in df_patient.columns:
    #     df_patient['admission_date_emerg'] = pd.to_datetime(df_patient['admission_date_emerg'],
    #                                                         format='%Y-%m-%d', errors='coerce')
    #     er_diag['timestamp'] = df_patient['admission_date_emerg'] + pd.Timedelta(hours=12)
    # else:
    #     raise ValueError("colonna 'admission_date_emerg' non trovata in patient_01.csv")
    # er_diag = er_diag.merge(df_patient[['patient_id', 'admission_date_emerg']], on='patient_id', how='left')
    # er_diag['timestamp'] = pd.to_datetime(er_diag['admission_date_emerg']+' 12:00:00')

    er_diag = er_diag.merge(df_patient[['patient_id', 'admission_date_emerg']],
                            on = 'patient_id', how = 'left')
    er_diag['timestamp'] = er_diag['admission_date_emerg'] + pd.Timedelta(hours=12)

    hosp_diag = pd.melt(df_diag_hosp,
                        id_vars=['patient_id'],
                        value_vars=[col for col in df_diag_er.columns if col.startswith('dia_')],
                        var_name='diag_num',
                        value_name='diagnosis')
    hosp_diag = hosp_diag.dropna(subset=['diagnosis'])
    hosp_diag['activity'] = 'DIAGNOSIS_HOSP_' + hosp_diag['diagnosis'].astype(str)  # .str[:50]

    # if 'admission_d_inpat' in df_patient.columns:
    #     df_patient['admission_d_inpat'] = pd.to_datetime(
    #         df_patient['admission_d_inpat'], format='%Y-%m-%d', errors='coerce'
    #     )

    hosp_diag = hosp_diag.merge(df_patient[['patient_id', 'admission_d_inpat']],
                                on='patient_id', how='left')

    hosp_diag['days_offset'] = hosp_diag.groupby('patient_id').cumcount()
    hosp_diag['timestamp'] = hosp_diag['admission_d_inpat'] + \
                                            pd.to_timedelta(hosp_diag['days_offset'], unit='h')
    # else:
    #     raise ValueError("Colonna 'admission_d_inpat' non trovata in patient_01.csv")

    df_vitals['constants_ing_time'] = df_vitals['constants_ing_time'].str.strip().fillna('00:00')
    df_vitals['constants_ing_time'] = df_vitals['constants_ing_time'].apply(
        lambda x:
        x if ':' in x else
        f"{x}:00" if x.replace(':', '').isdigit() else '00:00'
    )

    df_vitals['timestamp'] = pd.to_datetime(df_vitals['constants_ing_date'].astype(str)+
                                            ' ' + df_vitals['constants_ing_time'].astype(str),
                                            format='%Y-%m-%d %H:%M', errors='coerce')

    df_vitals.loc[df_vitals['timestamp'].isna(), 'timestamp'] = pd.to_datetime(
                    df_vitals['constants_ing_date'], errors='coerce')
    # try:
    #     # df_vitals['timestamp'] = pd.to_datetime(df_vitals['constants_ing_date'].astype(str) + ' ' +
    #     #                                         df_vitals['constants_ing_time'].astype(str),
    #     #                                         format='%Y-%m-%d %H:%M:%S')
    #
    #     df_vitals['date_part'] = pd.to_datetime(df_vitals['constants_ing_date'], format='%Y-%m-%d', errors='coerce')
    #     df_vitals['time_part'] = pd.to_datetime(df_vitals['constants_ing_time'], format='%H:%M:%S')
    #     df_vitals['timestamp'] = df_vitals['date_part'] + df_vitals['time_part']
    #     if df_vitals['timestamp'].isna().any():
    #         print(f"Warning: {df_vitals['timestamp'].isna().sum()} timestamp non validi")
    #
    #         df_vitals.loc[df_vitals['timestamp'].isna(), 'timestamp'] = pd.to_datetime(
    #             df_vitals['constants_ing_date'], errors='coerce')
    #
    #
    # except Exception as e:
    #     print(f"Errore nella creazione del timestamp: {e}")
    #     raise

    vital_events = df_vitals[['patient_id', 'timestamp']].copy()
    vital_events['activity'] = 'VITAL_MEASUREMENT'

    vital_events['bp'] = df_vitals['bp_max_ing'].astype(str) + '/' + df_vitals['bp_min_ing'].astype(str)
    vital_events['temp'] = df_vitals['temp_ing']
    vital_events['hr'] = df_vitals['hr_ing']
    vital_events['o2_sat'] = df_vitals['sat_02_ing']

    med_start = df_treat[['patient_id', 'drug_start_date', 'id_atc5']].copy()
    med_start['activity'] = 'MED_START_' + df_treat['id_atc5'].astype(str)
    med_start['timestamp'] = pd.to_datetime(med_start['drug_start_date'],errors='coerce')

    med_end = df_treat.dropna(subset=['drug_end_date'])[['patient_id', 'drug_end_date', 'id_atc5']].copy()
    med_end['activity'] = 'MED_END_' + med_end['id_atc5'].astype(str)
    med_end['timestamp'] = pd.to_datetime(med_end['drug_end_date'], errors='coerce')


    df_lab['time_lab'] = df_lab['time_lab'].fillna('00:00')
    df_lab['timestamp'] = pd.to_datetime(
        df_lab['lab_date'].astype(str) + ' ' + df_lab['time_lab'].astype(str),
        format='%Y-%m-%d %H:%M',
        errors='coerce')

    lab_events = df_lab[['patient_id', 'timestamp', 'item_lab']].copy()
    lab_events['activity'] = 'LAB_' + df_lab['item_lab'].astype(str)

    lab_events['result'] = df_lab['val_result'].fillna(df_lab['result_text'])

    event_log = pd.concat([
        admission_events[['patient_id', 'timestamp', 'activity']],
        icu_events[['patient_id', 'timestamp', 'activity']],
        discharge_events[['patient_id', 'timestamp', 'activity']],
        er_diag[['patient_id', 'timestamp', 'activity']],
        hosp_diag[['patient_id', 'timestamp', 'activity']],
        vital_events[['patient_id', 'timestamp', 'activity']],
        med_start[['patient_id', 'timestamp', 'activity']],
        med_end[['patient_id', 'timestamp', 'activity']],
        lab_events[['patient_id', 'timestamp', 'activity']]
    ])

    event_log = event_log.sort_values(['patient_id', 'timestamp'])

    event_log.columns = ['case_id', 'timestamp', 'activity']

    event_log = event_log.drop_duplicates().dropna(subset=['timestamp'])
    event_log.to_csv('/home/ubuntu/data_process_mining/event_log_covid.csv', index=False)
