""" Main FUNA_EMM Code """

import os

import experiment.analysis as an
import experiment.save_and_store_result as ssr


def main(data_name='', data_from=None, datasets_names=None, synthetic_params=None, sim_params=None, extra_info=None, date=None, output_to=''):
    """ Central function to run the analysis on the dataset. """
    # create path and empty output file
    output_to_path = output_to + data_name + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)
    excel_file_name, sheet_names = ssr.create_empty_output_file(
        output_to_path=output_to_path)

    if synthetic_params is None:
        an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sim_params=sim_params,
                    extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    # It never occurs
    # elif synthetic_params is not None:
    #     an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, data_from=data_from, sim_params=sim_params,
    #                           extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    ssr.final_update_result(
        excel_file_name=excel_file_name, sheet_names=sheet_names)


def main_test_cases(choice=0):
    """ Choosing which test case to run """
    output_path = 'output/DescriptiveLearning'
    current_date = '20250630'
    input_data_path = 'data_input'

    def choice_1a():  # FUNA
        """ Explanation of the test case #1a """
        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': True,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': True,
                'run_beam_search': True,
                'make_dfd': False,
                'm': None
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_1b():  # FUNA
        """ Explanation of the test case #1b """
        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': True,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': False,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 50
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_1c():  # FUNA
        """ Explanation of the test case #1c """
        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3],
                'q': [20],
                'model': ['subrange_ssrb'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.5],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': False,
                'sample_prop': None,

                'case_based_target': False,
                'run_redun_metrics': False,
                'run_beam_search': True,
                'make_dfd': False,
                'm': None
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_2a():  # FUNA
        """ Explanation of the test case #2a """

        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [5],
                'q': [10],
                'model': ['subrange_bic'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': True,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': True,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 2,
                'startorder': 0,

                'maxorder': 3
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_2b():  # FUNA
        """ Explanation of the test case #2b """
        # do ssr again, with 1/ef instead of ef
        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['subrange_ssr'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': True,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': True,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 50
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_2c():  # Curran
        """ Explanation of the test case #2c """
        main(
            data_name='Curran',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['reg_ssr', 'reg_ssrb', 'reg_bic'],
                'dbs': [False],
                'alpha': [0.05],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['read', 'id', 'occasion', 'kidagetv'],
                'sample': None,
                'prefclass': None,
                'case_based_target': False,
                'run_redun_metrics': True,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 2,
                'startorder': 0,

                'maxorder': 3
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_2d():  # FUNA
        """ Explanation of the test case #2d """
        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3],
                'q': [20],
                'model': ['subrange_bic'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.5],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': False,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': False,
                'run_beam_search': True,
                'make_dfd': False,
                'm': 2,
                'startorder': 0,
                'maxorder': 3
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_3():   # Curran
        """ Explanation of the test case #3 """

        main(
            data_name='Curran',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['reg_ssr', 'reg_ssrb', 'reg_bic'],
                'dbs': [False],
                'alpha': [0.05],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['read', 'id', 'occasion', 'kidagetv'],
                'sample': None,
                'prefclass': None,
                'case_based_target': False,
                'run_redun_metrics': False,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 50,
                'startorder': 0,
                'maxorder': 3
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    def choice_4():   # FUNA
        """ Explanation of the test case #4 """

        main(
            data_name='FUNA',
            datasets_names=['desc'],
            synthetic_params=None,
            sim_params={
                'b': [4],
                'w': [20],
                'd': [3, 5],
                'q': [10],
                'model': ['subrange_bic'],
                'dbs': [False],
                'wcs': [True],
                'gamma': [0.1, 0.5, 0.9],
                'dp': [False],
                'md': ['without'],
                'min_size': [0.05]
            },
            extra_info={
                'target_column_names': ['DMTime', 'IDCode', 'PreOrd', 'DMStimL'],
                'sample': True,
                'sample_prop': 0.05,

                'case_based_target': False,
                'run_redun_metrics': False,
                'run_beam_search': True,
                'make_dfd': True,
                'm': 50,
                'startorder': 0,
                'maxorder': 3
            },
            date=current_date,
            data_from=input_data_path,
            output_to=output_path
        )

    if choice == 1:
        choice_1a()
        choice_1b()
        choice_1c()
    elif choice == 2:
        choice_2a()
        choice_2b()
        choice_2c()
        choice_2d()
    elif choice == 3:
        choice_3()
    elif choice == 4:
        choice_4()
    else:
        error_msg = "Invalid choice. Please choose a number between 1 and 4."
        raise ValueError(error_msg)


if __name__ == '__main__':
    main_test_cases(choice=1)
    # main_test_cases(choice=2)
    # main_test_cases(choice=3)
    # main_test_cases(choice=4)
