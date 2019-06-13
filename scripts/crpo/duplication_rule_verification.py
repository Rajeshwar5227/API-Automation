import requests
import json
from hpro_automation.read_excel import *
import datetime
import xlrd
import time
from hpro_automation import (login, input_paths, output_paths, work_book)


class VerifyDuplicationRule(login.CRPOLogin, work_book.WorkBook):

    def __init__(self):
        self.start_time = str(datetime.datetime.now())
        super(VerifyDuplicationRule, self).__init__()

        self.Expected_success_cases = list(map(lambda x: 'Pass', range(0, 97)))
        self.Actual_Success_case = []
        self.success_case_01 = {}

        # print self.headers
        self.excelwriteheaders()
        file_path = input_paths.inputpaths['Duplication_rule_Input_sheet']
        duplicate_sheet_index = 0
        excel_read_obj.excel_read(file_path, duplicate_sheet_index)
        print(excel_read_obj.complete_excel_data)
        data = excel_read_obj.complete_excel_data
        tot = len(data)
        for iteration in range(0, tot):
            self.current_data = data[iteration]
            self.updateduplicaterule()
            self.checkDuplicate()

    def excelwriteheaders(self):

        self.ws.write(1, 0, 'Actual_Status', self.style2)
        self.ws.write(1, 1, 'Name', self.style0)
        self.ws.write(1, 2, 'Fname', self.style0)
        self.ws.write(1, 3, 'Mname', self.style0)
        self.ws.write(1, 4, 'Lname', self.style0)
        self.ws.write(1, 5, 'Email Address', self.style0)
        self.ws.write(1, 6, 'Mobile', self.style0)
        self.ws.write(1, 7, 'Phone', self.style0)
        self.ws.write(1, 8, 'Marital Status', self.style0)
        self.ws.write(1, 9, 'Gender', self.style0)
        self.ws.write(1, 10, 'DOB', self.style0)
        self.ws.write(1, 11, 'PANCARD', self.style0)
        self.ws.write(1, 12, 'PASSPORT', self.style0)
        self.ws.write(1, 13, 'Aadhar', self.style0)
        self.ws.write(1, 14, 'USN', self.style0)
        self.ws.write(1, 15, 'College', self.style0)
        self.ws.write(1, 16, 'Degree', self.style0)
        self.ws.write(1, 17, 'Location', self.style0)
        self.ws.write(1, 18, 'Total Experience(in Months)', self.style0)

        self.ws.write(1, 19, 'LinkedIn', self.style0)
        self.ws.write(1, 20, 'Facebook', self.style0)
        self.ws.write(1, 21, 'Twitter', self.style0)

        self.ws.write(1, 22, 'Text1', self.style0)
        self.ws.write(1, 23, 'Text2', self.style0)
        self.ws.write(1, 24, 'Text3', self.style0)
        self.ws.write(1, 25, 'Text4', self.style0)
        self.ws.write(1, 26, 'Text5', self.style0)
        self.ws.write(1, 27, 'Text6', self.style0)
        self.ws.write(1, 28, 'Text7', self.style0)
        self.ws.write(1, 29, 'Text8', self.style0)
        self.ws.write(1, 30, 'Text9', self.style0)
        self.ws.write(1, 31, 'Text10', self.style0)
        self.ws.write(1, 32, 'Text11', self.style0)
        self.ws.write(1, 33, 'Text12', self.style0)
        self.ws.write(1, 34, 'Text13', self.style0)
        self.ws.write(1, 35, 'Text14', self.style0)
        self.ws.write(1, 36, 'Text15', self.style0)

        self.ws.write(1, 37, 'Integer1', self.style0)
        self.ws.write(1, 38, 'Integer2', self.style0)
        self.ws.write(1, 39, 'Integer3', self.style0)
        self.ws.write(1, 40, 'Integer4', self.style0)
        self.ws.write(1, 41, 'Integer5', self.style0)
        self.ws.write(1, 42, 'Integer6', self.style0)
        self.ws.write(1, 43, 'Integer7', self.style0)
        self.ws.write(1, 44, 'Integer8', self.style0)
        self.ws.write(1, 45, 'Integer9', self.style0)
        self.ws.write(1, 46, 'Integer10', self.style0)
        self.ws.write(1, 47, 'Integer11', self.style0)
        self.ws.write(1, 48, 'Integer12', self.style0)
        self.ws.write(1, 49, 'Integer13', self.style0)
        self.ws.write(1, 50, 'Integer14', self.style0)
        self.ws.write(1, 51, 'Integer15', self.style0)
        self.ws.write(1, 52, 'Duplicate Rule', self.style2)

        self.ws.write(1, 53, 'Expected Status', self.style2)
        self.ws.write(1, 54, 'Actual Status', self.style2)
        self.ws.write(1, 55, 'Expected Message', self.style2)
        self.ws.write(1, 56, 'Actual Message', self.style2)
        # self.ws.write(0, 55, 'Message', self.__style0)

    def updateduplicaterule(self):
        self.update_json_data = self.current_data.get('DuplicationRuleJson')
        # print self.update_json_data
        self.data1 = {"AppPreference": {"Id": 3595, "Content": self.update_json_data,
                                        "Type": "duplication_conf.default"}, "IsTenantGlobal": "true"}
        r = requests.post("https://amsin.hirepro.in/py/common/common_app_utils/save_app_preferences/",
                          headers=self.get_token, data=json.dumps(self.data1, default=str), verify=False)
        # print r.content
        # print r.status_code

    def checkDuplicate(self):
        convert_date_of_birth = self.current_data.get('DateOfBirth')
        self.date_of_birth = datetime.datetime(
            *xlrd.xldate_as_tuple(convert_date_of_birth, excel_read_obj.excel_file.datemode))
        self.date_of_birth = self.date_of_birth.strftime("%Y-%m-%d")

        self.data = {"FirstName": self.current_data.get('FirstName'), "MiddleName": self.current_data.get('MiddleName'),
                     "LastName": self.current_data.get('LastName'),
                     "Email1": self.current_data.get('EmailAddress'),
                     "Mobile1": int(self.current_data.get('MobileNumber')) if self.current_data.get(
                         'MobileNumber') else None,
                     "PhoneOffice": int(self.current_data.get('PhoneNumber')) if self.current_data.get(
                         'PhoneNumber') else None,
                     "MaritalStatus": int(self.current_data.get('MaritalStatus')) if self.current_data.get(
                         'MaritalStatus') else None, "Gender": int(self.current_data.get('Gender')),
                     "DateOfBirth": self.date_of_birth,
                     "PanNo": self.current_data.get('Pancard'), "PassportNo": self.current_data.get('Passport'),
                     "AadhaarNo": int(self.current_data.get('Aadhar')) if self.current_data.get('Aadhar') else None,
                     "CollegeId": int(self.current_data.get('College')) if self.current_data.get('College') else None,
                     "DegreeId": int(self.current_data.get('Degree')) if self.current_data.get('Degree') else None,
                     "USN": self.current_data.get('USN'),
                     "CurrentLocationId": int(self.current_data.get('Location')) if self.current_data.get(
                         'Location') else None,
                     "TotalExperience": int(self.current_data.get('TotalExperienceInMonths')) if self.current_data.get(
                         'TotalExperienceInMonths') else None,
                     "FacebookLink": self.current_data.get('Facebook'),
                     "TwitterLink": self.current_data.get('Twitter'),
                     "LinkedInLink": self.current_data.get('LinkedIn'),
                     "Integer1": int(self.current_data.get('Integer1')) if self.current_data.get('Integer1') else None,
                     "Integer2": int(self.current_data.get('Integer2')) if self.current_data.get('Integer2') else None,
                     "Integer3": int(self.current_data.get('Integer3')) if self.current_data.get('Integer3') else None,
                     "Integer4": int(self.current_data.get('Integer4')) if self.current_data.get('Integer4') else None,
                     "Integer5": int(self.current_data.get('Integer5')) if self.current_data.get('Integer5') else None,
                     "Integer6": int(self.current_data.get('Integer6')) if self.current_data.get('Integer6') else None,
                     "Integer7": int(self.current_data.get('Integer7')) if self.current_data.get('Integer7') else None,
                     "Integer8": int(self.current_data.get('Integer8')) if self.current_data.get('Integer8') else None,
                     "Integer9": int(self.current_data.get('Integer9')) if self.current_data.get('Integer9') else None,
                     "Integer10": int(self.current_data.get('Integer10')) if self.current_data.get(
                         'Integer10') else None,
                     "Integer11": int(self.current_data.get('Integer11')) if self.current_data.get(
                         'Integer11') else None,
                     "Integer12": int(self.current_data.get('Integer12')) if self.current_data.get(
                         'Integer12') else None,
                     "Integer13": int(self.current_data.get('Integer13')) if self.current_data.get(
                         'Integer13') else None,
                     "Integer14": int(self.current_data.get('Integer14')) if self.current_data.get(
                         'Integer14') else None,
                     "Integer15": int(self.current_data.get('Integer15')) if self.current_data.get(
                         'Integer15') else None,
                     "Text1": self.current_data.get('Text1'), "Text2": self.current_data.get('Text2'),
                     "Text3": self.current_data.get('Text3'),
                     "Text4": self.current_data.get('Text4'), "Text5": self.current_data.get('Text5'),
                     "Text6": self.current_data.get('Text6'),
                     "Text7": self.current_data.get('Text7'), "Text8": self.current_data.get('Text8'),
                     "Text9": self.current_data.get('Text9'),
                     "Text10": self.current_data.get('Text10'), "Text11": self.current_data.get('Text11'),
                     "Text12": self.current_data.get('Text12'),
                     "Text13": self.current_data.get('Text13'), "Text14": self.current_data.get('Text14'),
                     "Text15": self.current_data.get('Text15')
                     }
        # print self.data

        r = requests.post("https://amsin.hirepro.in/py/rpo/candidate_duplicate_check/",
                          headers=self.get_token, data=json.dumps(self.data, default=str), verify=False)

        time.sleep(1)
        resp_dict = json.loads(r.content)
        self.is_duplicate = resp_dict["IsDuplicate"]
        # print self.is_duplicate
        self.message = resp_dict['Message']

        if self.is_duplicate:
            self.is_duplicate1 = "Duplicate"
            # print self.is_duplicate1
        else:
            self.is_duplicate1 = "NotDuplicate"
            # print self.is_duplicate1

        if self.is_duplicate1 == self.current_data.get('ExpectedOutput'):
            self.style6 = self.style14
        else:
            self.style6 = self.style13

        self.excelwrite(self.message)

    def excelwrite(self, message):

        if message == self.current_data.get('Message'):
            self.status = "Pass"
            style = self.style14
            self.ws.write(self.rowsize, 0, self.status, self.style26)
            self.success_case_01 = 'Pass'
        else:
            self.status = "Fail"
            style = self.style3
            self.ws.write(self.rowsize, 0, self.status, self.style3)

        self.ws.write(self.rowsize, 1, self.current_data.get('CandidateName'), self.style12)
        self.ws.write(self.rowsize, 2, self.current_data.get('FirstName'), self.style12)
        self.ws.write(self.rowsize, 3, self.current_data.get('MiddleName'), self.style12)
        self.ws.write(self.rowsize, 4, self.current_data.get('LastName'), self.style12)
        self.ws.write(self.rowsize, 5, self.current_data.get('EmailAddress'), self.style12)
        self.ws.write(self.rowsize, 6, self.current_data.get('MobileNumber'), self.style12)
        self.ws.write(self.rowsize, 7, self.current_data.get('PhoneNumber'), self.style12)
        self.ws.write(self.rowsize, 8, self.current_data.get('MaritalStatus'), self.style12)
        self.ws.write(self.rowsize, 9, self.current_data.get('Gender'), self.style12)
        self.ws.write(self.rowsize, 10, self.date_of_birth, self.style12)
        self.ws.write(self.rowsize, 11, self.current_data.get('Pancard'), self.style12)
        self.ws.write(self.rowsize, 12, self.current_data.get('Passport'), self.style12)
        self.ws.write(self.rowsize, 13, self.current_data.get('Aadhar'), self.style12)
        self.ws.write(self.rowsize, 14, self.current_data.get('USN'), self.style12)
        self.ws.write(self.rowsize, 15, self.current_data.get('College'), self.style12)
        self.ws.write(self.rowsize, 16, self.current_data.get('Degree'), self.style12)
        self.ws.write(self.rowsize, 17, self.current_data.get('Location'), self.style12)
        self.ws.write(self.rowsize, 18, self.current_data.get('TotalExperienceInMonths'), self.style12)

        self.ws.write(self.rowsize, 19, self.current_data.get('LinkedIn'), self.style12)
        self.ws.write(self.rowsize, 20, self.current_data.get('Facebook'), self.style12)
        self.ws.write(self.rowsize, 21, self.current_data.get('Twitter'), self.style12)

        self.ws.write(self.rowsize, 22, self.current_data.get('Text1'), self.style12)
        self.ws.write(self.rowsize, 23, self.current_data.get('Text2'), self.style12)
        self.ws.write(self.rowsize, 24, self.current_data.get('Text3'), self.style12)
        self.ws.write(self.rowsize, 25, self.current_data.get('Text4'), self.style12)
        self.ws.write(self.rowsize, 26, self.current_data.get('Text5'), self.style12)
        self.ws.write(self.rowsize, 27, self.current_data.get('Text6'), self.style12)
        self.ws.write(self.rowsize, 28, self.current_data.get('Text7'), self.style12)
        self.ws.write(self.rowsize, 29, self.current_data.get('Text8'), self.style12)
        self.ws.write(self.rowsize, 30, self.current_data.get('Text9'), self.style12)
        self.ws.write(self.rowsize, 31, self.current_data.get('Text10'), self.style12)
        self.ws.write(self.rowsize, 32, self.current_data.get('Text11'), self.style12)
        self.ws.write(self.rowsize, 33, self.current_data.get('Text12'), self.style12)
        self.ws.write(self.rowsize, 34, self.current_data.get('Text13'), self.style12)
        self.ws.write(self.rowsize, 35, self.current_data.get('Text14'), self.style12)
        self.ws.write(self.rowsize, 36, self.current_data.get('Text15'), self.style12)

        self.ws.write(self.rowsize, 37, self.current_data.get('Integer1'), self.style12)
        self.ws.write(self.rowsize, 38, self.current_data.get('Integer2'), self.style12)
        self.ws.write(self.rowsize, 39, self.current_data.get('Integer3'), self.style12)
        self.ws.write(self.rowsize, 40, self.current_data.get('Integer4'), self.style12)
        self.ws.write(self.rowsize, 41, self.current_data.get('Integer5'), self.style12)
        self.ws.write(self.rowsize, 42, self.current_data.get('Integer6'), self.style12)
        self.ws.write(self.rowsize, 43, self.current_data.get('Integer7'), self.style12)
        self.ws.write(self.rowsize, 44, self.current_data.get('Integer8'), self.style12)
        self.ws.write(self.rowsize, 45, self.current_data.get('Integer9'), self.style12)
        self.ws.write(self.rowsize, 46, self.current_data.get('Integer10'), self.style12)
        self.ws.write(self.rowsize, 47, self.current_data.get('Integer11'), self.style12)
        self.ws.write(self.rowsize, 48, self.current_data.get('Integer12'), self.style12)
        self.ws.write(self.rowsize, 49, self.current_data.get('Integer13'), self.style12)
        self.ws.write(self.rowsize, 50, self.current_data.get('Integer14'), self.style12)
        self.ws.write(self.rowsize, 51, self.current_data.get('Integer15'), self.style12)
        self.ws.write(self.rowsize, 52, self.current_data.get('DuplicationRuleText'), self.style12)

        self.ws.write(self.rowsize, 53, self.current_data.get('ExpectedOutput'), self.style12)
        self.ws.write(self.rowsize, 54, self.is_duplicate1, self.style14)

        self.ws.write(self.rowsize, 55, self.current_data.get('Message'), self.style12)

        self.ws.write(self.rowsize, 56, message, style)

        self.rowsize = self.rowsize + 1
        self.wb_Result.save(output_paths.outputpaths['Duplication_rule_Output_sheet'])

        if self.success_case_01 == 'Pass':
            self.Actual_Success_case.append(self.success_case_01)

        self.success_case_01 = {}

    def overall_status(self):
        self.ws.write(0, 0, 'Duplication Check', self.style23)
        if self.Expected_success_cases == self.Actual_Success_case:
            self.ws.write(0, 1, 'Pass', self.style24)
        else:
            self.ws.write(0, 1, 'Fail', self.style25)

        self.ws.write(0, 3, 'Start Time', self.style23)
        self.ws.write(0, 4, self.start_time, self.style26)
        ob.wb_Result.save(output_paths.outputpaths['Duplication_rule_Output_sheet'])


ob = VerifyDuplicationRule()
ob.overall_status()
