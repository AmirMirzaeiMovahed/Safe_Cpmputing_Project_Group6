import os
import subprocess
import platform
import pandas as pd
import cx_Oracle

file_path = r'C:\Users\IP3\Desktop\Safe_Computing_project_Group6\Safe_Computing_project_Group6\Basic Excel files\Oracle Database 11g Instance STIG-MAC-3_Sensitive.xlsx'

def connect_to_oracle():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="ORCL")
    connection = cx_Oracle.connect(user="sys", password="13821382", dsn=dsn, mode=cx_Oracle.SYSDBA)
    return connection

# V-2554
def check_v_2554(connection):
    cursor = connection.cursor()

    query = "SELECT VALUE FROM V$PARAMETER WHERE NAME = 'remote_os_authent'"
    cursor.execute(query)
    result = cursor.fetchone()

    if not result or result[0] != 'FALSE':
        return "Fail"

    return "Done"


# V-2555
def check_v_2555(connection):
    cursor = connection.cursor()

    query = "SELECT VALUE FROM V$PARAMETER WHERE NAME = 'remote_os_roles'"
    cursor.execute(query)
    result = cursor.fetchone()

    if not result or result[0] != 'FALSE':
        return "Fail"

    return "Done"


# V-15635
def check_v_15635(connection):
    cursor = connection.cursor()

    # in this query, there is exactly 704 default password list and their decoded value
    query1 = """
    SELECT name, 
           DECODE(astatus,
                  0, 'OPEN',
                  1, 'EXPIRED',
                  2, 'EXPIRED(GRACE)',
                  4, 'LOCKED(TIMED)',
                  8, 'LOCKED',
                  5, 'EXPIRED and LOCKED(TIMED)',
                  6, 'EXPIRED(GRACE) and LOCKED(TIMED)',
                  9, 'EXPIRED and LOCKED',
                  10, 'EXPIRED(GRACE) and LOCKED') AS account_status
    FROM sys.user$
    WHERE name <> 'XS$NULL'
        AND (password = DECODE(name,
            'AASH', '9B52488370BB3D77',
            'ABA1', '30FD307004F350DE',
            'ABM', 'D0F2982F121C7840',
            'AD_MONITOR', '54F0C83F51B03F49',
            'ADAMS', '72CDEF4A3483F60D',
            'ADS', 'D23F0F5D871EB69F',
            'ADSEUL_US', '4953B2EB6FCB4339',
            'AHL', '7910AE63C9F7EEEE',
            'AHM', '33C2E27CF5E401A4',
            'AK', '8FCB78BBA8A59515',
            'AL', '384B2C568DE4C2B5',
            'ALA1', '90AAC5BD7981A3BA',
            'ALLUSERS', '42F7CD03B7D2CA0F',
            'ALR', 'BE89B24F9F8231A9',
            'AMA1', '585565C23AB68F71',
            'AMA2', '37E458EE1688E463',
            'AMA3', '81A66D026DC5E2ED',
            'AMA4', '194CCC94A481DCDE',
            'AMF', 'EC9419F55CDC666B',
            'AMS', 'BD821F59270E5F34',
            'AMS1', 'DB8573759A76394B',
            'AMS2', 'EF611999C6AD1FD7',
            'AMS3', '41D1084F3F966440',
            'AMS4', '5F5903367FFFB3A3',
            'AMSYS', '4C1EF14ECE13B5DE',
            'AMV', '38BC87EB334A1AC4',
            'AMW', '0E123471AACA2A62',
            'ANNE', '1EEA3E6F588599A6',
            'ANONYMOUS', '94C33111FD9C66F3',
            'AOLDEMO', 'D04BBDD5E643C436',
            'AP', 'EED09A552944B6AD',
            'APA1', 'D00197BF551B2A79',
            'APA2', '121C6F5BD4674A33',
            'APA3', '5F843C0692560518',
            'APA4', 'BF21227532D2794A',
            'APPLEAD', '5331DB9C240E093B',
            'APPLSYS', '0F886772980B8C79',
            'APPLSYSPUB', 'D2EEF40EE87221E',
            'APPLSYS', 'E153FFF4DAE6C9F7',
            'APPS', 'D728438E8A5925E0',
            'APS1', 'F65751C55EA079E6',
            'APS2', '5CACE7B928382C8B',
            'APS3', 'C786695324D7FB3B',
            'APS4', 'F86074C4F4F82D2C',
            'AQDEMO', '5140E342712061DD',
            'AQJAVA', '8765D2543274B42E',
            'AQUSER', '4CF13BDAC1D7511C',
            'AR', 'BBBFE175688DED7E',
            'ARA1', '4B9F4E0667857EB8',
            'ARA2', 'F4E52BFBED4652CD',
            'ARA3', 'E3D8D73AE399F7FE',
            'ARA4', '758FD31D826E9143',
            'ARS1', '433263ED08C7A4FD',
            'ARS2', 'F3AF9F26D0213538',
            'ARS3', 'F6755F08CC1E7831',
            'ARS4', '452B5A381CABB241',
            'ART', '665168849666C4F3',
            'ASF', 'B6FD427D08619EEE',
            'ASG', '1EF8D8BD87CF16BE',
            'ASL', '03B20D2C323D0BFE',
            'ASN', '1EE6AEBD9A23D4E0',
            'ASO', 'F712D80109E3C9D8',
            'ASP', 'CF95D2C6C85FF513',
            'AST', 'F13FF949563EAB3C',
            'AUC_GUEST', '8A59D349DAEC26F7',
            'AURORA$ORB$UNAUTHENTICATED', '80C099F0EADF877E',
            'AUTHORIA', 'CC78120E79B57093',
            'AX', '0A8303530E86FCDD',
            'AZ', 'AAA18B5D51B0D5AC',
            'B2B', 'CC387B24E013C616',
            'BAM', '031091A1D1A30061',
            'BCA1', '398A69209360BD9D',
            'BCA2', '801D9C90EBC89371',
            'BEN', '9671866348E03616',
            'BIC', 'E84CC95CBBAC1B67',
            'BIL', 'BF24BCE2409BE1F7',
            'BIM', '6026F9A8A54B9468',
            'BIS', '7E9901882E5F3565',
            'BIV', '2564B34BE50C2524',
            'BIX', '3DD36935EAEDE2E3',
            'BLAKE', '9435F2E60569158E',
            'BMEADOWS', '2882BA3D3EE1F65A',
            'BNE', '080B5C7EE819BF78',
            'BOM', '56DB3E89EAE5788E',
            'BP01', '612D669D2833FACD',
            'BP02', 'FCE0C089A3ECECEE',
            'BP03', '0723FFEEFBA61545',
            'BP04', 'E5797698E0F8934E',
            'BP05', '58FFC821F778D7E9',
            'BP06', '2F358909A4AA6059',
            'BSC', 'EC481FD7DCE6366A',
            'BUYACCT', 'D6B388366ECF2F61',
            'BUYAPPR1', 'CB04931693309228',
            'BUYAPPR2', '3F98A3ADC037F49C',
            'BUYAPPR3', 'E65D8AD3ACC23DA3',
            'BUYER', '547BDA4286A2ECAE',
            'BUYMTCH', '0DA5E3B504CC7497',
            'CAMRON', '4384E3F9C9C9B8F1',
            'CANDICE', 'CF458B3230215199',
            'CARL', '99ECCC664FFDFEA2',
            'CARLY', 'F7D90C099F9097F1',
            'CARMEN', '46E23E1FD86A4277',
            'CARRIECONYERS', '9BA83B1E43A5885B',
            'CATADMIN', 'AF9AB905347E004F',
            'CE', 'E7FDFE26A524FE39',
            'CAESAR', 'E69833B8205D5DD7',
            'CENTRA', '63BF5FFE5E3EA16D',
            'CFD', '667B018D4703C739',
            'CHANDRA', '184503FA7786C82D',
            'CHARLEY', 'E500DAA705382E8D',
            'CHRISBAKER', '52AFB6B3BE485F81',
            'CHRISTIE', 'C08B79CCEC43E798',
            'CINDY', '3AB2C717D1BD0887',
            'CLARK', '7AAFE7D01511D73F',
            'CLAUDE', 'C6082BCBD0B69D20',
            'CLARK', '74DF527800B6D713',
            'CLINT', '163FF8CCB7F11691',
            'CLN', 'A18899D42066BFCA',
            'CN', '73F284637A54777D',
            'CNCADMIN', 'C7C8933C678F7BF9',
            'CONNIE', '982F4C420DD38307',
            'CONNOR', '52875AEB74008D78',
            'CORY', '93CE4CCE632ADCD2',
            'CRM1', '6966EA64B0DFC44E',
            'CRM2', 'B041F3BEEDA87F72',
            'CRP', 'F165BDE5462AD557',
            'CRPB733', '2C9AB93FF2999125',
            'CRPCTL', '4C7A200FB33A531D',
            'CRPDTA', '6665270166D613BC',
            'CS', 'DB78866145D4E1C3',
            'CSADMIN', '94327195EF560924',
            'CSAPPR1', '47D841B5A01168FF',
            'CSC', 'EDECA9762A8C79CD',
            'CSD', '144441CEBAFC91CF',
            'CSDUMMY', '7A587C459B93ACE4',
            'CSE', 'D8CC61E8F42537DA',
            'CSF', '684E28B3C899D42C',
            'CSI', '71C2B12C28B79294',
            'CSL', 'C4D7FE062EFB85AB',
            'CSM', '94C24FC0BE22F77F',
            'CSMIG', '09B4BB013FBD0D65',
            'CSP', '5746C5E077719DB4',
            'CSR', '0E0F7C1B1FE3FA32',
            'CSS', '3C6B8C73DDC6B04F',
            'CTXDEMO', 'CB6B5E9D9672FE89',
            'CTXSYS', '24ABAB8B06281B4C',
            'CTXTEST', '064717C317B551B6',
            'CTXSYS', '71E687F036AD56E5',
            'CUA', 'CB7B2E6FFDD7976F',
            'CUE', 'A219FE4CA25023AA',
            'CUF', '82959A9BD2D51297',
            'CUG', '21FBCADAEAFCC489',
            'CUI', 'AD7862E01FA80912',
            'CUN', '41C2D31F3C85A79D',
            'CUP', 'C03082CD3B13EC42',
            'CUS', '00A12CC6EBF8EDB8',
            'CZ', '9B667E9C5A0D21A6',
            'DAVIDMORGAN', 'B717BAB262B7A070',
            'DBSNMP', 'E066D214D5421CCC',
            'DCM', '45CCF86E1058D3A5',
            'DD7333', '44886308CF32B5D4',
            'DD7334', 'D7511E19D9BD0F90',
            'DD810', '0F9473D8D8105590',
            'DD811', 'D8084AE609C9A2FD',
            'DD812', 'AB71915CF21E849E',
            'DD9', 'E81821D03070818C',
            'DDB733', '7D11619CEE99DE12',
            'DDD', '6CB03AF4F6DD133D',
            'DEMO8', '0E7260738FDFD678',
            'DES', 'ABFEC5AC2274E54D',
            'DES2K', '611E7A73EC4B425A',
            'DEV2000_DEMOS', '18A0C8BD6B13BEE2',
            'DEVB733', '7500DF89DC99C057',
            'DEVUSER', 'C10B4A80D00CA7A5',
            'DGRAY', '5B76A1EB8F212B85',
            'DIP', 'CE4A36B8E06CA59C',
            'DISCOVERER5', 'AF0EDB66D914B731',
            'DKING', '255C2B0E1F0912EA',
            'DLD', '4454B932A1E0E320',
            'DMADMIN', 'E6681A8926B40826',
            'DMATS', '8C692701A4531286',
            'DMS', '1351DC7ED400BD59',
            'DMSYS', 'BFBA5A553FD9E28A',
            'DOM', '51C9F2BECA78AE0E',
            'DPOND', '79D6A52960EEC216',
            'DSGATEWAY', '6869F3CFD027983A',
            'DV7333', '36AFA5CD674BA841',
            'DV7334', '473B568021BDB428',
            'DV810', '52C38F48C99A0352',
            'DV811', 'B6DC5AAB55ECB66C',
            'DV812', '7359E6E060B945BA',
            'DV9', '07A1D03FD26E5820',
            'DVP1', '0559A0D3DE0759A6',
            'EAA', 'A410B2C5A0958CDF',
            'EAM', 'CE8234D92FCFB563',
            'EC', '6A066C462B62DD46',
            'ECX', '0A30645183812087',
            'EDR', '5FEC29516474BB3A',
            'EDWEUL_US', '5922BA2E72C49787',
            'EDWREP', '79372B4AB748501F',
            'EGC1', 'D78E0F2BE306450D',
            'EGD1', 'DA6D6F2089885BA6',
            'EGM1', 'FB949D5E4B5255C0',
            'EGO', 'B9D919E5F5A9DA71',
            'EGR1', 'BB636336ADC5824A',
            'END1', '688499930C210B75',
            'ENG', '4553A3B443FB3207',
            'ENI', '05A92C0958AFBCBC',
            'ENM1', '3BDABFD1246BFEA2',
            'ENS1', 'F68A5D0D6D2BB25B',
            'ENTMGR_CUST', '45812601EAA2B8BD',
            'ENTMGR_PRO', '20002682991470B3',
            'ENTMGR_TRAIN', 'BE40A3BE306DD857',
            'EOPP_PORTALADM', 'B60557FD8C45005A',
            'EOPP_PORTALMGR', '9BB3CF93F7DE25F1',
            'EOPP_USER', '13709991FC4800A1',
            'EUL_US', '28AEC22561414B29',
            'EVM', '137CEDC20DE69F71',
            'EXA1', '091BCD95EE112EE3',
            'EXA2', 'E4C0A21DBD06B890',
            'EXA3', '40DC4FA801A73560',
            'EXA4', '953885D52BDF5C86',
            'EXFSYS', '66F4EF5650C20355',
            'EXS1', 'C5572BAB195817F0',
            'EXS2', '8FAA3AC645793562',
            'EXS3', 'E3050174EE1844BA',
            'EXS4', 'E963BFE157475F7D',
            'FA', '21A837D0AED8F8E5',
            'FEM', 'BD63D79ADF5262E7',
            'FIA1', '2EB76E07D3E094EC',
            'FII', 'CF39DE29C08F71B9',
            'FLM', 'CEE2C4B59E7567A3',
            'FNI1', '308839029D04F80C',
            'FNI2', '05C69C8FEAB4F0B9',
            'FPA', '9FD6074B9FD3754C',
            'FPT', '73E3EC9C0D1FAECF',
            'FRM', '9A2A7E2EBE6E4F71',
            'FTA1', '65FF9AB3A49E8A13',
            'FTE', '2FB4D2C9BAE2CCCA',
            'FUN', '8A7055CA462DB219',
            'FV', '907D70C0891A85B1',
            'FVP1', '6CC7825EADF994E8',
            'GALLEN', 'F8E8ED9F15842428',
            'GCA1', '47DA9864E018539B',
            'GCA2', 'FD6E06F7DD50E868',
            'GCA3', '4A4B9C2E9624C410',
            'GCA9', '48A7205A4C52D6B5',
            'GCMGR1', '14A1C1A08EA915D6',
            'GCMGR2', 'F4F11339A4221A4D',
            'GCMGR3', '320F0D4258B9D190',
            'GCS', '7AE34CA7F597EBF7',
            'GCS1', '2AE8E84D2400E61D',
            'GCS2', 'C242D2B83162FF3D',
            'GCS3', 'DCCB4B49C68D77E2',
            'GEORGIAWINE', 'F05B1C50A1C926DE',
            'GL', 'CD6E99DACE4EA3A6',
            'GLA1', '86C88007729EB36F',
            'GLA2', '807622529F170C02',
            'GLA3', '863A20A4EFF7386B',
            'GLA4', 'DB882CF89A758377',
            'GLS1', '7485C6BD564E75D1',
            'GLS2', '319E08C55B04C672',
            'GLS3', 'A7699C43BB136229',
            'GLS4', '7C171E6980BE2DB9',
            'GM_AWDA', '4A06A107E7A3BB10',
            'GM_COPI', '03929AE296BAAFF2',
            'GM_DPHD', '0519252EDF68FA86',
            'GM_MLCT', '24E8B569E8D1E93E',
            'GM_PLADMA', '2946218A27B554D8',
            'GM_PLADMH', '2F6EDE96313AF1B7',
            'GM_PLCCA', '7A99244B545A038D',
            'GM_PLCCH', '770D9045741499E6',
            'GM_PLCOMA', '91524D7DE2B789A8',
            'GM_PLCOMH', 'FC1C6E0864BF0AF2',
            'GM_PLCONA', '1F531397B19B1E05',
            'GM_PLCONH', 'C5FE216EB8FCD023',
            'GM_PLNSCA', 'DB9DD2361D011A30',
            'GM_PLNSCH', 'C80D557351110D51',
            'GM_PLSCTA', '3A778986229BA20C',
            'GM_PLSCTH', '9E50865473B63347',
            'GM_PLVET', '674885FDB93D34B9',
            'GM_SPO', 'E57D4BD77DAF92F0',
            'GM_STKH', 'C498A86BE2663899',
            'GMA', 'DC7948E807DFE242',
            'GMD', 'E269165256F22F01',
            'GME', 'B2F0E221F45A228F',
            'GMF', 'A07F1956E3E468E1',
            'GMI', '82542940B0CF9C16',
            'GML', '5F1869AD455BBA73',
            'GMP', '450793ACFCC7B58E',
            'GMS', 'E654261035504804',
            'GR', 'F5AB0AA3197AEE42',
            'GUEST', '1C0A090E404CECD0',
            'HCC', '25A25A7FEFAC17B6',
            'HHCFO', '62DF37933FB35E9F',
            'HR', '4C6D73C3E8B0F0DA',
            'HRI', '49A3A09B8FC291D0',
            'HXC', '4CEA0BF02214DA55',
            'HXT', '169018EB8E2C4A77',
            'IA', '42C7EAFBCEEC09CC',
            'IBA', '0BD475D5BF449C63',
            'IBC', '9FB08604A30A4951',
            'IBE', '9D41D2B3DD095227',
            'IBP', '840267B7BD30C82E',
            'IBU', '0AD9ABABC74B3057',
            'IBY', 'F483A48F6A8C51EC',
            'ICX', '7766E887AF4DCC46',
            'IEB', 'A695699F0F71C300',
            'IEC', 'CA39F929AF0A2DEC',
            'IEM', '37EF7B2DD17279B5',
            'IEO', 'E93196E9196653F1',
            'IES', '30802533ADACFE14',
            'IEU', '5D0E790B9E882230',
            'IEX', '6CC978F56D21258D',
            'IGC', 'D33CEB8277F25346',
            'IGF', '1740079EFF46AB81',
            'IGI', '8C69D50E9D92B9D0',
            'IGS', 'DAF602231281B5AC',
            'IGW', 'B39565F4E3CF744B',
            'IMC', 'C7D0B9CDE0B42C73',
            'IMT', 'E4AAF998653C9A72',
            'INS1', '2ADC32A0B154F897',
            'INS2', 'EA372A684B790E2A',
            'INTERNET_APPSERVER_REGISTRY', 'A1F98A977FFD73CD',
            'INV', 'ACEAB015589CF4BC',
            'IP', 'D29012C144B58A40',
            'IPA', 'EB265A08759A15B4',
            'IPD', '066A2E3072C1F2F3',
            'ISC', '373F527DC0CFAE98',
            'ISTEWARD', '8735CA4085DE3EEA',
            'ITG', 'D90F98746B68E6CA',
            'JA', '9AC2B58153C23F3D',
            'JD7333', 'FB5B8A12AE623D52',
            'JD7334', '322810FCE43285D9',
            'JD9', '9BFAEC92526D027B',
            'JDE', '7566DC952E73E869',
            'JDEDBA', 'B239DD5313303B1D',
            'JE', 'FBB3209FD6280E69',
            'JG', '37A99698752A1CF1',
            'JL', '489B61E488094A8D',
            'JOHNINARI', 'B3AD4DA00F9120CE',
            'JONES', 'B9E99443032F059D',
            'JTF', '5C5F6FC2EBB94124',
            'JTI', 'B8F03D3E72C96F7',
            'JTM', '6D79A2259D5B4B5A',
            'JTR', 'B4E2BE38B556048F',
            'JTS', '4087EE6EB7F9CD7C',
            'JUNK_PS', 'BBC38DB05D2D3A7A',
            'JUSTOSHUM', '53369CD63902FAAA',
            'KELLYJONES', 'DD4A3FF809D2A6CF',
            'KEVINDONS', '7C6D9540B45BBC39',
            'KPN', 'DF0AED05DE318728',
            'LADAMS', 'AE542B99505CDCD2',
            'LBA', '18E5E15A436E7157',
            'LBACSYS', 'AC9700FD3F1410EB',
            'LDQUAL', '1274872AB40D4FCD',
            'LHILL', 'E70CA2CA0ED555F5',
            'LNS', 'F8D2BC61C10941B2',
            'LQUINCY', '13F9B9C1372A41B6',
            'LSA', '2D5E6036E3127B7E',
            'MDDATA', 'DF02A496267DEE66',
            'MDSYS', '72979A94BAD2AF80',
            'ME', 'E5436F7169B29E4D',
            'MDSYS', '9AAEB2214DCC9A31',
            'MFG', 'FC1B0DD35E790847',
            'MGR1', 'E013305AB0185A97',
            'MGR2', '5ADE358F8ACE73E8',
            'MGR3', '05C365C883F1251A',
            'MGR4', 'E229E942E8542565',
            'MIKEIKEGAMI', 'AAF7A168C83D5C47',
            'MJONES', 'EE7BB3FEA50A21C5',
            'MLAKE', '7EC40274AC1609CA',
            'MM1', '4418294570E152E7',
            'MM2', 'C06B5B28222E1E62',
            'MM3', 'A975B1BD0C093DA3',
            'MM4', '88256901EB03A012',
            'MM5', '4CEA62CBE776DCEC',
            'MMARTIN', 'D52F60115FE87AA4',
            'MOBILEADMIN', '253922686A4A45CC',
            'MRP', 'B45D4DF02D4E0C85',
            'MSC', '89A8C104725367B2',
            'MSD', '6A29482069E23675',
            'MSO', '3BAA3289DB35813C',
            'MSR', 'C9D53D00FE77D813',
            'MST', 'A96D2408F62BE1BC',
            'MWA', '1E2F06BE2A1D41A6',
            'NEILKATSU', '1F625BB9FEBC7617',
            'OBJ7333', 'D7BDC9748AFEDB52',
            'OBJ7334', 'EB6C5E9DB4643CAC',
            'OBJB733', '61737A9F7D54EF5F',
            'OCA', '9BC450E4C6569492',
            'ODM', 'C252E8FA117AF049',
            'ODM_MTR', 'A7A32CD03D3CE8D5',
            'ODS', '89804494ADFC71BC',
            'ODSCOMMON', '59BBED977430C1A8',
            'OE', 'D1A2DFC623FDA40A',
            'OKB', 'A01A5F0698FC9E31',
            'OKC', '31C1DDF4D5D63FE6',
            'OKE', 'B7C1BB95646C16FE',
            'OKI', '991C817E5FD0F35A',
            'OKL', 'DE058868E3D2B966',
            'OKO', '6E204632EC7CA65D',
            'OKR', 'BB0E28666845FCDC',
            'OKS', 'C2B4C76AB8257DF5',
            'OKX', 'F9FDEB0DE52F5D6B',
            'OL810', 'E2DA59561CBD0296',
            'OL811', 'B3E88767A01403F8',
            'OL812', 'AE8C7989346785BA',
            'OL9', '17EC83E44FB7DB5B',
            'OLAPSYS', '3FB8EF9DB538647C',
            'ONT', '9E3C81574654100A',
            'OPI', '1BF23812A0AEEDA0',
            'ORABAM', 'D0A4EA93EF21CE25',
            'ORABAMSAMPLES', '507F11063496F222',
            'ORABPEL', '26EFDE0C9C051988',
            'ORAESB', 'CC7FCCB3A1719EDA',
            'ORAOCA_PUBLIC', 'FA99021634DDC111',
            'ORASAGENT', '234B6F4505AD8F25',
            'ORASSO', 'F3701A008AA578CF',
            'ORASSO_DS', '17DC8E02BC75C141',
            'ORASSO_PA', '133F8D161296CB8F',
            'ORASSO_PS', '63BB534256053305',
            'ORASSO_PUBLIC', 'C6EED68A8F75F5D3',
            'ORDPLUGINS', '88A2B2C183431F00',
            'ORDSYS', '7EFA02EC7EA6B86F',
            'OSM', '106AE118841A5D8C',
            'OTA', 'F5E498AC7009A217',
            'OUTLN', '4A3BA55E08595C81',
            'OWAPUB', '6696361B64F9E0A9',
            'OWF_MGR', '3CBED37697EB01D1',
            'OZF', '970B962D942D0C75',
            'OZP', 'B650B1BB35E86863',
            'OZS', '0DABFF67E0D33623',
            'PA', '8CE2703752DB36D8',
            'PABLO', '5E309CB43FE2C2FF',
            'PAIGE', '02B6B704DFDCE620',
            'PAM', '1383324A0068757C',
            'PARRISH', '79193FDACFCE46F6',
            'PARSON', 'AE28B2BD64720CD7',
            'PAT', 'DD20769D59F4F7BF',
            'PATORILY', '46B7664BD15859F9',
            'PATRICKSANCHEZ', '47F74BD3AD4B5F0A',
            'PATSY', '4A63F91FEC7980B7',
            'PAUL', '35EC0362643ADD3F',
            'PAULA', 'BB0DC58A94C17805',
            'PAXTON', '4EB5D8FAD3434CCC',
            'PCA1', '8B2E303DEEEEA0C0',
            'PCA2', '7AD6CE22462A5781',
            'PCA3', 'B8194D12FD4F537D',
            'PCA4', '83AD05F1D0B0C603',
            'PCS1', '2BE6DD3D1DEA4A16',
            'PCS2', '78117145145592B1',
            'PCS3', 'F48449F028A065B1',
            'PCS4', 'E1385509C0B16BED',
            'PD7333', '5FFAD8604D9DC00F',
            'PD7334', 'CDCF262B5EE254E1',
            'PD810', 'EB04A177A74C6BCB',
            'PD811', '3B3C0EFA4F20AC37',
            'PD812', 'E73A81DB32776026',
            'PD9', 'CACEB3F9EA16B9B7',
            'PDA1', 'C7703B70B573D20F',
            'PEARL', 'E0AFD95B9EBD0261',
            'PEG', '20577ED9A8DB8D22',
            'PENNY', 'BB6103E073D7B811',
            'PEOPLE', '613459773123B38A',
            'PERCY', 'EB9E8B33A2DDFD11',
            'PERRY', 'D62B14B93EE176B6',
            'PETE', '4040619819A9C76E',
            'PEYTON', 'B7127140004677FC',
            'PHIL', '181446AE258EE2F6',
            'PJI', '5024B1B412CD4AB9',
            'PJM', '021B05DBB892D11F',
            'PM', '72E382A52E89575A',
            'PMI', 'A7F7978B21A6F65E',
            'PN', 'D40D0FEF9C8DC624',
            'PO', '355CBEC355C10FEF',
            'POA', '2AB40F104D8517A0',
            'POLLY', 'ABC770C112D23DBE',
            'POM', '123CF56E05D4EF3C',
            'PON', '582090FD3CC44DA3',
            'PORTAL', 'A96255A27EC33614',
            'PORTAL_APP', '831A79AFB0BD29EC',
            'PORTAL_DEMO', 'A0A3A6A577A931A3',
            'PORTAL_PUBLIC', '70A9169655669CE8',
            'PORTAL30', '969F9C3839672C6D',
            'PORTAL30_DEMO', 'CFD1302A7F832068',
            'PORTAL30_PUBLIC', '42068201613CA6E2',
            'PORTAL30_SSO', '882B80B587FCDBC8',
            'PORTAL30_SSO_PS', 'F2C3DC8003BC90F8',
            'PORTAL30_SSO_PUBLIC', '98741BDA2AC7FFB2',
            'POS', '6F6675F272217CF7',
            'PPM1', 'AA4AE24987D0E84B',
            'PPM2', '4023F995FF78077C',
            'PPM3', '12F56FADDA87BBF9',
            'PPM4', '84E17CB7A3B0E769',
            'PPM5', '804C159C660F902C',
            'PRISTB733', '1D1BCF8E03151EF5',
            'PRISTCTL', '78562A983A2F78FB',
            'PRISTDTA', '3FCBC379C8FE079C',
            'PRODB733', '9CCD49EB30CB80C4',
            'PRODCTL', 'E5DE2F01529AE93C',
            'PRODDTA', '2A97CD2281B256BA',
            'PRODUSER', '752E503EFBF2C2CA',
            'PROJMFG', '34D61E5C9BC7147E',
            'PRP', 'C1C4328F8862BC16',
            'PS', '0AE52ADF439D30BD',
            'PS810', '90C0BEC7CA10777E',
            'PS810CTL', 'D32CCE5BDCD8B9F9',
            'PS810DTA', 'AC0B7353A58FC778',
            'PS811', 'B5A174184403822F',
            'PS811CTL', '18EDE0C5CCAE4C5A',
            'PS811DTA', '7961547C7FB96920',
            'PS812', '39F0304F007D92C8',
            'PS812CTL', 'E39B1CE3456ECBE5',
            'PS812DTA', '3780281C933FE164',
            'PSA', 'FF4B266F9E61F911',
            'PSB', '28EE1E024FC55E66',
            'PSBASS', 'F739804B718D4406',
            'PSEM', '40ACD8C0F1466A57',
            'PSFT', '7B07F6F3EC08E30D',
            'PSFTDBA', 'E1ECD83073C4E134',
            'PSP', '4FE07360D435E2F0',
            'PTADMIN', '4C35813E45705EBA',
            'PTCNE', '463AEFECBA55BEE8',
            'PTDMO', '251D71390034576A',
            'PTE', '380FDDB696F0F266',
            'PTESP', '5553404C13601916',
            'PTFRA', 'A360DAD317F583E3',
            'PTG', '7AB0D62E485C9A3D',
            'PTGER', 'C8D1296B4DF96518',
            'PTJPN', '2159C2EAF20011BF',
            'PTUKE', 'D0EF510BCB2992A3',
            'PTUPG', '2C27080C7CC57D06',
            'PTWEB', '8F7F509D4DC01DF6',
            'PTWEBSERVER', '3C8050536003278B',
            'PUBLIC', '',
            'PV', '76224BCC80895D3D',
            'PY7333', '2A9C53FE066B852F',
            'PY7334', 'F3BBFAE0DDC5F7AC',
            'PY810', '95082D35E94B88C2',
            'PY811', 'DC548D6438E4D6B7',
            'PY812', '99C575A55E9FDA63',
            'PY9', 'B8D4E503D0C4FCFD',
            'QA', 'C7AEAA2D59EB1EAE',
            'QOT', 'B27D0E5BA4DC8DEA',
            'QP', '10A40A72991DCA15',
            'QRM', '098286E4200B22DE',
            'QS', '4603BCD2744BDE4F',
            'QS_ADM', '3990FB418162F2A0',
            'QS_CB', '870C36D8E6CD7CF5',
            'QS_CBADM', '20E788F9D4F1D92C',
            'QS_CS', '2CA6D0FC25128CF3',
            'QS_ES', '9A5F2D9F5D1A9EF4',
            'QS_OS', '0EF5997DC2638A61',
            'QS_WS', '0447F2F756B4F460',
            'RENE', '9AAD141AB0954CF0',
            'REPADMIN', '915C93F34954F5F8',
            'REPORTS', '0D9D14FE6653CF69',
            'REPORTS_USER', '635074B4416CD3AC',
            'RESTRICTED_US', 'E7E67B60CFAFBB2D',
            'RG', '0FAA06DA0F42F21F',
            'RHX', 'FFDF6A0C8C96E676',
            'RLA', 'C1959B03F36C9BB2',
            'RLM', '4B16ACDA351B557D',
            'RM1', 'CD43500DAB99F447',
            'RM2', '2D8EE7F8857D477E',
            'RM3', '1A95960A95AC2E1D',
            'RM4', '651BFD4E1DE4B040',
            'RM5', 'FDCC34D74A22517C',
            'RMAN', 'E7B5D92911C831E1',
            'ROB', '94405F516486CA24',
            'RPARKER', 'CEBFE4C41BBCC306',
            'RWA1', 'B07E53895E37DBBB',
            'SALLYH', '21457C94616F5716',
            'SAM', '4B95138CB6A4DB94',
            'SARAHMANDY', '60BE21D8711EE7D9',
            'SCM1', '507306749131B393',
            'SCM2', 'CBE8D6FAC7821E85',
            'SCM3', '2B311B9CDC70F056',
            'SCM4', '1FDF372790D5A016',
            'SCOTT', 'F894844C34402B67',
            'SDAVIS', 'A9A3B88C6A550559',
            'SECDEMO', '009BBE8142502E10',
            'SEDWARDS', '00A2EDFD7835BC43',
            'SELLCM', '8318F67F72276445',
            'SELLER', 'B7F439E172D5C3D0',
            'SELLTREAS', '6EE7BA85E9F84560',
            'SERVICES', 'B2BE254B514118A5',
            'SETUP', '9EA55682C163B9A3',
            'SH', '54B253CBBAAA8C48',
            'SI_INFORMTN_SCHEMA', '84B8CBCA4D477FA3',
            'SID', 'CFA11E6EBA79D33E',
            'SKAYE', 'ED671B63BDDB6B50',
            'SKYTETSUKA', 'EB5DA777D1F756EC',
            'SLSAA', '99064FC6A2E4BBE8',
            'SLSMGR', '0ED44093917BE294',
            'SLSREP', '847B6AAB9471B0A5',
            'SRABBITT', '85F734E71E391DF5',
            'SRALPHS', '975601AA57CBD61A',
            'SRAY', 'C233B26CFC5DC643',
            'SRIVERS', '95FE94ADC2B39E08',
            'SSA1', 'DEE6E1BEB962AA8B',
            'SSA2', '96CA278B20579E34',
            'SSA3', 'C3E8C3B002690CD4',
            'SSC1', '4F7AC652CC728980',
            'SSC2', 'A1350B328E74AE87',
            'SSC3', 'EE3906EC2DA586D8',
            'SSOSDK', '7C48B6FF3D54D006',
            'SSP', '87470D6CE203FB4D',
            'SSS1', 'E78C515C31E83848',
            'SUPPLIER', '2B45928C2FE77279',
            'SVM7333', '04B731B0EE953972',
            'SVM7334', '62E2A2E886945CC8',
            'SVM810', '0A3DCD8CA3B6ABD9',
            'SVM811', '2B0CD57B1091C936',
            'SVM812', '778632974E3947C9',
            'SVM9', '552A60D8F84441F1',
            'SVMB733', 'DD2BFB14346146FE',
            'SVP1', 'F7BF1FFECE27A834',
            'SY810', 'D56934CED7019318',
            'SY811', '2FDC83B401477628',
            'SY812', '812B8D7211E7DEF1',
            'SY9', '3991E64C4BC2EC5D',
            'SYS', '43CA255A7916ECFE',
            'SYS7333', 'D7CDB3124F91351E',
            'SYS', '5638228DAF52805F',
            'SYS7334', '06959F7C9850F1E3',
            'SYS', 'D4C5016086B2DC6A',
            'SYSADMIN', 'DC86E8DEAA619C1A',
            'SYSB733', '7A7F5C90BEC02F0E',
            'SYSMAN', 'EB258E708132DD2D',
            'SYSTEM', '4D27CA6E3E3066E6',
            'TDEMARCO', 'CAB71A14FA426FAE',
            'SYSTEM', 'D4DF7931AB130E37',
            'TDOS_ICSAP', '7C0900F751723768',
            'TESTCTL', '205FA8DF03A1B0A6',
            'TESTDTA', 'EEAF97B5F20A3FA3',
            'TRA1', 'BE8EDAE6464BA413',
            'TRACESVR', 'F9DA8977092B7B81',
            'TRBM1', 'B10ED16CD76DBB60',
            'TRCM1', '530E1F53715105D0',
            'TRDM1', 'FB1B8EF14CF3DEE7',
            'TRRM1', '4F29D85290E62EBE',
            'TWILLIAMS', '6BF819CE663B8499',
            'UDDISYS', 'BF5E56915C3E1C64',
            'VEA', 'D38D161C22345902',
            'VEH', '72A90A786AAE2914',
            'VIDEO31', '2FA72981199F9B97',
            'VIDEO4', '9E9B1524C454EEDE',
            'VIDEO5', '748481CFF7BE98BB',
            'VP1', '3CE03CD65316DBC7',
            'VP2', 'FCCEFD28824DFEC5',
            'VP3', 'DEA4D8290AA247B2',
            'VP4', 'F4730B0FA4F701DC',
            'VP5', '7DD67A696734AE29',
            'VP6', '45660DEE49534ADB',
            'WAA1', 'CF013DC80A9CBEE3',
            'WAA2', '6160E7A17091741A',
            'WCRSYS', '090263F40B744BD8',
            'WEBDB', 'D4C4DCDD41B05A5D',
            'WEBSYS', '54BA0A1CB5994D64',
            'WENDYCHO', '7E628CDDF051633A',
            'WH', '91792EFFCB2464F9',
            'WIP', 'D326D25AE0A0355C',
            'WIRELESS', '1495D279640E6C3A',
            'WK_TEST', '29802572EB547DBF',
            'WIRELESS', 'EB9615631433603E',
            'WKPROXY', 'AA3CB2A4D9188DDB',
            'WKSYS', '545E13456B7DDEA0',
            'WMS', 'D7837F182995E381',
            'WMSYS', '7C9BA362F8314299',
            'WPS', '50D22B9D18547CF7',
            'WSH', 'D4D76D217B02BD7A',
            'WSM', '750F2B109F49CC13',
            'XDB', '88D8364765FCE6AF',
            'XDO', 'E9DDE8ACFA7FE8E4',
            'XDP', 'F05E53C662835FA2',
            'XLA', '2A8ED59E27D86D41',
            'XLE', 'CEEBE966CC6A3E39',
            'XNB', '03935918FA35C993',
            'XNC', 'BD8EA41168F6C664',
            'XNI', 'F55561567EF71890',
            'XNM', '92776EA17B8B5555',
            'XNP', '3D1FB783F96D1F5E',
            'XNS', 'FABA49C38150455E',
            'XTR', 'A43EE9629FA90CAE',
            'YCAMPOS', 'C3BBC657F099A10F',
            'YSANCHEZ', 'E0C033C4C8CC9D84',
            'ZFA', '742E092A27DDFB77',
            'ZPB', 'CAF58375B6D06513',
            'ZSA', 'AFD3BD3C7987CBB6',
            'ZX', '7B06550956254585',
            'FLOWS_030000', 'B5C7B17C2C983E8F',
            'FLOWS_FILES', '5CDD1E40E516FE6A',
            'TSMSYS', '3DF26A8B17D0F29F',
            'ORACLE_OCM', '6D17CF1EB1611F94',
            'OWBSYS', '610A3C38F301776F',
            'SPATIAL_CSW_ADMIN', '093913703800E437',
            'SPATIAL_WFS_ADMIN', '32FA36DC781579AA',
            'SPATIAL_CSW_ADMIN_USR', '1B290858DD14107E',
            'SPATIAL_WFS_ADMIN_USR', '7117215D6BEE6E82',
            'MGMT_VIEW', '17028530E6D346B4',
            'APEX_PUBLIC_USER', 'C8E264D926F001D8',
            'XS$NULL', 'DC4FCC8CB69A6733',
            name)
        )
    """
    cursor.execute(query1)
    accounts = cursor.fetchall()
    result = all(
        (account_status in ['LOCKED', 'LOCKED(TIMED)', 'EXPIRED and LOCKED', 'EXPIRED and LOCKED(TIMED)']) or ("LOCKED" in account_status) or ("EXPIRED" in account_status)
        for _, account_status in accounts
    )

    if result :
        return "Done"
    else:
        return "Fail"


# V-3810
def check_v_3810(connection):
    cursor = connection.cursor()
    query = """
    SELECT username, authentication_type
    FROM dba_users
    WHERE account_status = 'OPEN'
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    non_pki_users = [row[0] for row in rows if row[1] not in ('PKI', 'CERTIFICATE')]
    return "Fail" if non_pki_users else "Done"


# V-16033
def check_v_16033(connection):
    cursor = connection.cursor()
    query = "SELECT value FROM v$parameter WHERE name = 'sec_case_sensitive_logon'"
    cursor.execute(query)
    result = cursor.fetchone()
    return "Done" if result and result[0] == 'TRUE' else "Fail"


# V-3817
def check_v_3817(connection):
    cursor = connection.cursor()
    query = r"""
    WITH default_limit AS (
        SELECT 
            CASE 
                WHEN limit = 'UNLIMITED' THEN 10
                WHEN limit = 'DEFAULT' THEN 10
                WHEN REGEXP_LIKE(limit, '^\d+$') THEN TO_NUMBER(limit)
                ELSE NULL
            END AS def_login_attempts
        FROM dba_profiles
        WHERE profile = 'DEFAULT' AND resource_name = 'FAILED_LOGIN_ATTEMPTS'
    )
    SELECT profile, 
           CASE 
               WHEN limit = 'UNLIMITED' THEN 10
               WHEN limit = 'DEFAULT' THEN (SELECT def_login_attempts FROM default_limit)
               WHEN REGEXP_LIKE(limit, '^\d+$') THEN TO_NUMBER(limit)
               ELSE NULL
           END AS resolved_limit
    FROM dba_profiles
    WHERE resource_name = 'FAILED_LOGIN_ATTEMPTS'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for profile, resolved_limit in results:
        if resolved_limit is None or resolved_limit > 3:
            return "Fail"
    return "Done"


# v-3815
def check_v_3815(connection):
    cursor = connection.cursor()

    try:
        # بررسی پروفایل‌های پایگاه داده و تابع تایید رمز عبور
        query_profiles = """
            SELECT profile, limit 
            FROM dba_profiles
            WHERE resource_name = 'PASSWORD_VERIFY_FUNCTION'
              AND limit NOT IN ('NULL', 'DEFAULT')
            ORDER BY profile
        """
        cursor.execute(query_profiles)
        rows = cursor.fetchall()

        if not rows:
            return "Fail"

        # نمایش تغییر رمز عبور و بررسی منطق تابع تایید رمز عبور
        query_function = """
            SELECT text 
            FROM dba_source
            WHERE name = 'PASSWORD_VERIFY_FUNCTION'
            ORDER BY line
        """
        cursor.execute(query_function)
        function_code = "".join(row[0] for row in cursor.fetchall())

        # بررسی منطق تابع تایید رمز عبور
        if "differ <= 4" in function_code and "raise_application_error(-20004" in function_code:
            return "Done"
        else:
            return "Fail"

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return "Fail"

    finally:
        cursor.close()


# V-15637
def check_v_15637(connection):
    cursor = connection.cursor()
    query = """
        SELECT object_name, object_type
        FROM dba_objects
        WHERE object_type IN ('PROCEDURE', 'FUNCTION')
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return "Fail"


#v-15633
def check_v_15633(connection):
    cursor = connection.cursor()
    query = """
        SELECT p1.profile, p1.limit AS REUSE_MAX, p2.limit AS REUSE_TIME
        FROM dba_profiles p1
        JOIN dba_profiles p2
          ON p1.profile = p2.profile
        WHERE p1.resource_name = 'PASSWORD_REUSE_MAX'
          AND p2.resource_name = 'PASSWORD_REUSE_TIME'
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for _, reuse_max, reuse_time in results:
        # بررسی شرایط UNLIMITED یا DEFAULT
        if reuse_max.upper() in ['UNLIMITED', 'DEFAULT'] or reuse_time.upper() in ['UNLIMITED', 'DEFAULT']:
            return "Fail"  # فقط Fail چاپ شود

    return "Done"


# V-2558
def check_v_2558(connection):
    cursor = connection.cursor()
    query = "SELECT VALUE FROM V$PARAMETER WHERE NAME = 'remote_login_passwordfile'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result and result[0] in ['EXCLUSIVE', 'NONE']:
        return "Done"
    else:
        return "Fail"


# V-15639
def check_v_15639(connection):
    cursor = connection.cursor()
    query = "SELECT profile, limit FROM dba_profiles WHERE resource_name = 'PASSWORD_LOCK_TIME'"
    cursor.execute(query)
    profiles = cursor.fetchall()
    if any(limit not in ['UNLIMITED', 'DEFAULT'] for _, limit in profiles):
        return "Fail"
    return "Done"


# V-15634
def check_v_15634(connection):
    cursor = connection.cursor()
    try:
        query_profiles = """
        SELECT profile FROM dba_profiles 
        WHERE resource_name = 'PASSWORD_VERIFY_FUNCTION' AND limit IS NULL
        """
        cursor.execute(query_profiles)
        profiles_without_function = cursor.fetchall()
        if profiles_without_function:
            return "Fail"

        user_query = "SELECT username FROM dba_users WHERE authentication_type = 'PASSWORD'"
        cursor.execute(user_query)
        users = cursor.fetchall()
        if not users:
            return "Fail"

        return "Done"
    except cx_Oracle.DatabaseError as e:
        print(f"Error during check_v_15634: {e}")
        return "Error"
    finally:
        cursor.close()


def check_v_15613(connection):
    """
    بررسی حساب های DBMS بر اساس الزامات امنیتی.
    """
    authorized_accounts = {"user1", "user2", "user3"}  # لیست حساب های مجاز را در اینجا وارد کنید

    cursor = connection.cursor()
    cursor.execute("""SELECT username, account_status FROM dba_users""")
    dbms_accounts = cursor.fetchall()
    cursor.close()

    for username, account_status in dbms_accounts:
        if account_status != 'OPEN':  # حساب های بسته را نادیده می گیریم
            continue

        if username not in authorized_accounts:
            return "Fail"

        # بررسی حساب های اشتراکی
        if "app" in username:
            return "Fail"

    return "Done"


# v-2520
def check_v_2520(connection):
    """
    بررسی اتصالات از راه دور به پایگاه داده.
    """
    authorized_connections = {"user1", "user2", "user3"}

    cursor = connection.cursor()

    # استخراج اتصالات از راه دور از پایگاه داده
    cursor.execute("""SELECT owner, db_link FROM dba_db_links""")
    remote_connections = cursor.fetchall()

    # بررسی اتصالات غیرمجاز
    for owner, db_link in remote_connections:
        if db_link not in authorized_connections:
            cursor.close()
            return "Fail"

    # بررسی استفاده از اتصالات برای Replication
    cursor.execute("""SELECT COUNT(*) FROM sys.dba_repcatlog""")
    replication_count = cursor.fetchone()[0]
    if replication_count > 0:
        cursor.close()
        return "Fail"

    cursor.close()
    return "Done"


# v-2527
def check_v_2527(connection):
    """
    بررسی نقش های DBA در پایگاه داده.
    """
    authorized_dba_accounts = {"user1", "user2", "user3"}

    cursor = connection.cursor()

    # استخراج کاربران با نقش DBA از پایگاه داده
    cursor.execute("""
        SELECT grantee
        FROM dba_role_privs
        WHERE granted_role = 'DBA'
        AND grantee NOT IN ('SYS', 'SYSTEM', 'SYSMAN', 'CTXSYS', 'WKSYS')
    """)
    dba_accounts = [grantee for grantee, in cursor.fetchall()]

    # بررسی حساب های DBA غیرمجاز
    for account in dba_accounts:
        if account not in authorized_dba_accounts:
            cursor.close()
            return "Fail"

        # بررسی حساب های توسعه دهنده
        if "dev" in account.lower():
            cursor.close()
            return "Fail"

        # بررسی حساب های مشترک
        if "shared" in account.lower():
            cursor.close()
            return "Fail"

    cursor.close()
    return "Done"


# V-15615
def check_v_15615(connection):
    cursor = connection.cursor()
    query = r"""
    SELECT username 
    FROM v$pwfile_users
    WHERE username NOT IN (
        SELECT grantee 
        FROM dba_role_privs 
        WHERE granted_role = 'DBA'
    )
    AND username <> 'INTERNAL'
    AND (sysdba = 'TRUE' OR sysoper = 'TRUE')
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return "Fail" if result else "Done"


# V-2516
def check_v_2516(connection):
    cursor = connection.cursor()

    # Check if replication is installed
    query_replication_objects = r"""
    SELECT COUNT(*) 
    FROM all_tables 
    WHERE table_name LIKE 'REPCAT%'
    """
    cursor.execute(query_replication_objects)
    replication_objects_count = cursor.fetchone()[0]

    if replication_objects_count == 0:
        return "Done"

    # Check if replication is in use
    query_replication_usage = r"""
    SELECT COUNT(*) 
    FROM sys.dba_repcatlog
    """
    cursor.execute(query_replication_usage)
    replication_usage_count = cursor.fetchone()[0]

    if replication_usage_count == 0:
        return "Done"

    # Additional checks must be manual
    return "ّFail"


# V-2593
def check_v_2593(connection):
    cursor = connection.cursor()
    query = "SELECT VALUE FROM V$PARAMETER WHERE NAME = 'resource_limit'"
    cursor.execute(query)
    result = cursor.fetchone()

    return "Done" if result and result[0] == 'TRUE' else "Fail"


# v-15152
def check_v_15152(connection):
    cursor = connection.cursor()
    query = "SELECT profile, limit FROM dba_profiles WHERE resource_name = 'PASSWORD_VERIFY_FUNCTION'"
    cursor.execute(query)
    profiles = cursor.fetchall()

    if any(limit is None for _, limit in profiles):
        return "Fail"

    return "Done"


# v-15153
def check_v_15153(connection):
    cursor = connection.cursor()

    # Check DEFAULT profile
    query_default = "SELECT limit FROM dba_profiles WHERE profile = 'DEFAULT' AND resource_name = 'PASSWORD_LIFE_TIME'"
    cursor.execute(query_default)
    default_limit = cursor.fetchone()
    if default_limit and (default_limit[0] == 'UNLIMITED' or int(default_limit[0]) > 60):
        return "Fail"

    # Non-default profiles
    query_non_default = "SELECT profile, limit FROM dba_profiles WHERE profile != 'DEFAULT' AND resource_name = 'PASSWORD_LIFE_TIME'"
    cursor.execute(query_non_default)
    non_default_profiles = cursor.fetchall()

    for _, limit in non_default_profiles:
        if limit == 'UNLIMITED' or (limit and int(limit) > 60):
            return "Fail"

    return "Done"


# v-2424
def check_v_2424(connection):
    cursor = connection.cursor()
    query = "SELECT username FROM dba_users ORDER BY username"
    cursor.execute(query)

    shared_accounts = []
    for (username,) in cursor.fetchall():
        if username in ['BATCHJOB', 'FMAPP', 'FMAPP-ADMIN']:
            shared_accounts.append(username)

    return shared_accounts if shared_accounts else "Fail"


def save_results(results):
    df = pd.read_excel(file_path)

    # Ensure the 'Result' column is initialized
    if "Result" not in df.columns:
        df["Result"] = None

    df["Result"] = df["Result"].astype(object)

    for code, result in results.items():
        if isinstance(result, list):  # Handle cases with multiple shared accounts
            result_string = ', '.join(result)
            df.loc[df["id"] == code, "Result"] = f"Shared Accounts: {
                result_string}"
        else:
            df.loc[df["id"] == code, "Result"] = result

    df.to_excel(file_path, index=False)


# V-3818
def check_v_3818(connection):
    cursor = connection.cursor()

    # Query to retrieve all database links and their hosts
    query = "SELECT db_link, host FROM dba_db_links"
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return "Done"

    # this part should complete by developer based on actual authorized links
    # Simulate a check against authorized database links (to be documented externally)
    # Replace `authorized_links` with the actual authorized links or fetch from documentation
    authorized_links = {
        "DBMS_CLRDBLINK": "ORACLR_CONNECTION_DATA",
        "Another Link": "Another Host",
    }

    unauthorized_links = []
    for link, host in results:
        if authorized_links.get(link) != host:
            unauthorized_links.append((link, host))
            print(link, " = ", host)

    if unauthorized_links:
        return "Fail"

    return "Done"


# V-15644
def check_v_15644(connection):
    cursor = connection.cursor()

    # Query to check for audit options that are not configured
    query = """
    SELECT name 
    FROM stmt_audit_option_map
    WHERE name NOT IN (
        SELECT audit_option 
        FROM dba_stmt_audit_opts
    )
    AND name NOT IN (
        'ALL STATEMENTS', 'ANALYZE ANY DICTIONARY',
        'CREATE DIRECTORY', 'DEBUG CONNECT ANY',
        'DEBUG CONNECT USER', 'DELETE ANY TABLE',
        'DELETE TABLE', 'DROP DIRECTORY',
        'EXECUTE ANY LIBRARY', 'EXECUTE ANY PROCEDURE',
        'EXECUTE ANY TYPE', 'EXECUTE LIBRARY',
        'EXECUTE PROCEDURE', 'EXISTS', 'GRANT LIBRARY',
        'INSERT ANY TABLE', 'INSERT TABLE', 'LOCK TABLE',
        'NETWORK', 'OUTLINE', 'READUP', 'READUP DBHIGH',
        'SELECT ANY DICTIONARY', 'SELECT ANY SEQUENCE',
        'SELECT ANY TABLE', 'SELECT MINING MODEL',
        'SELECT SEQUENCE', 'SELECT TABLE',
        'UPDATE ANY TABLE', 'UPDATE TABLE', 'USE EDITION',
        'WRITEDOWN', 'WRITEDOWN DBLOW', 'WRITEUP',
        'WRITEUP DBHIGH'
    )
    """

    query2 = """
    SELECT name 
    FROM stmt_audit_option_map
    WHERE name NOT IN (
        SELECT audit_option 
        FROM dba_stmt_audit_opts
    )
    AND name NOT IN (
        'LOCK TABLE', 'SELECT ANY DICTIONARY', 'EXECUTE LIBRARY', 'OUTLINE', 'USE EDITION', 'EXECUTE ANY LIBRARY',
        'DELETE ANY TABLE', 'SELECT ANY SEQUENCE', 'NETWORK', 'EXECUTE ANY TYPE', 'SELECT ANY TABLE', 'DELETE TABLE',
        'SELECT MINING MODEL', 'UPDATE TABLE', 'INSERT ANY TABLE', 'EXECUTE ANY PROCEDURE', 'ALL STATEMENTS',
        'SELECT SEQUENCE', 'EXECUTE PROCEDURE', 'INSERT TABLE', 'ANALYZE ANY DICTIONARY', 'UPDATE ANY TABLE',
        'SELECT TABLE','DROP ANY SYNONYM', 'DROP ANY INDEXTYPE', 'DELETE ANY CUBE DIMENSION', 'EXECUTE ANY INDEXTYPE',
        'SYNONYM', 'SELECT ANY MINING MODEL', 'ALTER MINING MODEL', 'ADMINISTER RESOURCE MANAGER', 'DIRECTORY',
        'CREATE ANY CONTEXT', 'ADMINISTER ANY SQL TUNING SET', 'DROP ANY INDEX', 'SYSOPER', 'CREATE TABLE',
        'MINING MODEL', 'ALTER ANY SQL PROFILE', 'ALTER ANY INDEX', 'FLASHBACK ARCHIVE ADMINISTER', 'USER',
        'DELETE ANY MEASURE FOLDER', 'MATERIALIZED VIEW', 'ALTER ROLLBACK SEGMENT', 'ALTER SEQUENCE',
        'EXECUTE ANY RULE SET', 'EXPORT FULL DATABASE', 'CREATE SEQUENCE', 'DROP ANY DIMENSION', 'CREATE VIEW',
        'CREATE TABLESPACE', 'DROP ANY TYPE', 'CREATE CLUSTER', 'EXECUTE ASSEMBLY', 'DROP ROLLBACK SEGMENT',
        'DROP ANY CUBE', 'DROP ANY DIRECTORY', 'ALTER ANY INDEXTYPE', 'CREATE MEASURE FOLDER', 'ALTER RESOURCE COST',
        'ALTER ANY OPERATOR', 'EXECUTE ANY CLASS', 'ALTER ANY CLUSTER', 'ADVISOR', 'CREATE RULE SET',
        'DROP JAVA RESOURCE', 'ALTER JAVA RESOURCE', 'CREATE ANY CUBE BUILD PROCESS', 'DROP ANY ROLE',
        'ALTER JAVA CLASS', 'CLUSTER', 'PROCEDURE', 'ALTER ANY OUTLINE', 'ALTER ANY RULE SET', 'ALTER ANY RULE',
        'CREATE ANY OUTLINE', 'EXECUTE ANY EVALUATION CONTEXT', 'READ ANY FILE GROUP', 'INSERT ANY MEASURE FOLDER',
        'TRIGGER', 'ALTER ANY EVALUATION CONTEXT', 'DROP JAVA CLASS', 'EXECUTE ANY PROGRAM', 'CREATE ANY CLUSTER',
        'CREATE ANY TRIGGER', 'DROP ANY ASSEMBLY', 'CREATE CUBE BUILD PROCESS', 'CREATE ANY MEASURE FOLDER',
        'COMMENT ANY TABLE', 'CREATE ANY INDEX', 'CREATE ANY TYPE', 'CHANGE NOTIFICATION', 'MANAGE TABLESPACE',
        'CREATE ANY INDEXTYPE', 'QUERY REWRITE', 'ADMINISTER SQL MANAGEMENT OBJECT', 'GRANT EDITION',
        'ENQUEUE ANY QUEUE', 'DROP ANY MEASURE FOLDER', 'CREATE ANY EDITION', 'DROP ANY OPERATOR', 'CREATE LIBRARY',
        'DROP PUBLIC SYNONYM', 'TABLESPACE', 'CREATE ANY DIRECTORY', 'CREATE JOB', 'SEQUENCE', 'DEBUG PROCEDURE',
        'DROP ANY RULE SET', 'DROP ANY SQL PROFILE', 'ALTER JAVA SOURCE', 'DROP TABLESPACE', 'CREATE ANY SQL PROFILE',
        'CREATE ANY RULE', 'DROP PUBLIC DATABASE LINK', 'ADMINISTER SQL TUNING SET', 'GRANT MINING MODEL', 'TYPE',
        'INDEX', 'ADMINISTER DATABASE TRIGGER', 'MANAGE SCHEDULER', 'ALTER ANY CUBE', 'RESTRICTED SESSION',
        'DIRECT_PATH UNLOAD', 'AUDIT ANY', 'MANAGE ANY FILE GROUP', 'FORCE ANY TRANSACTION', 'LOCK ANY TABLE',
        'GRANT PROCEDURE', 'ALTER ANY SEQUENCE', 'ALTER ANY LIBRARY', 'DEBUG ANY PROCEDURE', 'ROLLBACK SEGMENT',
        'CREATE JAVA SOURCE', 'BECOME USER', 'GRANT DIRECTORY', 'CREATE PUBLIC SYNONYM', 'DIMENSION',
        'INSERT ANY CUBE DIMENSION', 'MERGE ANY VIEW', 'SELECT ANY CUBE', 'CREATE OPERATOR', 'CREATE MINING MODEL',
        'ALTER ANY ROLE', 'CREATE ROLLBACK SEGMENT', 'CREATE ANY EVALUATION CONTEXT', 'NOT EXISTS',
        'CREATE MATERIALIZED VIEW', 'COMMENT TABLE', 'DROP ANY LIBRARY', 'DIRECT_PATH LOAD', 'DROP ANY RULE',
        'DEBUG CONNECT SESSION', 'CREATE ANY OPERATOR', 'UPDATE ANY CUBE', 'CREATE PROFILE', 'GRANT TABLE',
        'ALTER ANY TYPE', 'VIEW', 'DROP ANY EVALUATION CONTEXT', 'ALTER ANY MATERIALIZED VIEW', 'ALTER ANY MINING MODEL',
        'EXEMPT IDENTITY POLICY', 'GRANT TYPE', 'CREATE ANY CUBE', 'ON COMMIT REFRESH', 'EXECUTE ANY OPERATOR',
        'CREATE CUBE DIMENSION', 'ALTER DATABASE LINK', 'ALTER TABLE', 'DROP ANY CONTEXT', 'ALTER ANY EDITION',
        'DROP ANY OUTLINE', 'CREATE ANY RULE SET', 'EXECUTE ANY ASSEMBLY', 'UNLIMITED TABLESPACE', 'IMPORT FULL DATABASE',
        'COMMENT ANY MINING MODEL', 'CREATE ANY MATERIALIZED VIEW', 'DROP ANY EDITION', 'DROP ANY CLUSTER',
        'CREATE ANY SEQUENCE', 'ANALYZE ANY', 'SYSDBA', 'ALTER TABLESPACE', 'FORCE TRANSACTION', 'COMMENT MINING MODEL',
        'CREATE JAVA CLASS', 'CREATE ANY CUBE DIMENSION', 'CREATE ASSEMBLY', 'TABLE', 'COMMENT EDITION',
        'UPDATE ANY CUBE BUILD PROCESS', 'DROP ANY MATERIALIZED VIEW', 'UPDATE ANY CUBE DIMENSION', 'UNDER ANY VIEW',
        'CREATE ANY DIMENSION', 'CREATE ANY SYNONYM', 'CREATE ANY MINING MODEL', 'CREATE INDEXTYPE', 'CREATE TYPE',
        'DROP ANY TRIGGER', 'BACKUP ANY TABLE', 'CREATE EVALUATION CONTEXT', 'CREATE TRIGGER', 'CREATE RULE', 'RESUMABLE',
        'CREATE CUBE', 'CREATE JAVA RESOURCE', 'UNDER ANY TABLE', 'MANAGE ANY QUEUE', 'ALTER ANY CUBE DIMENSION',
        'CREATE ANY ASSEMBLY', 'DROP JAVA SOURCE', 'FLASHBACK ANY TABLE', 'CREATE DIMENSION', 'DROP ANY CUBE BUILD PROCESS',
        'ALTER ANY TRIGGER', 'SELECT ANY TRANSACTION', 'DROP ANY CUBE DIMENSION', 'ALTER ANY DIMENSION', 'CREATE SYNONYM',
        'CREATE PROCEDURE', 'ALTER ANY ASSEMBLY', 'PUBLIC DATABASE LINK', 'EXECUTE ANY RULE', 'CREATE DATABASE LINK',
        'SELECT ANY CUBE DIMENSION', 'CREATE ANY VIEW', 'UNDER ANY TYPE', 'MANAGE FILE GROUP', 'GRANT SEQUENCE',
        'CREATE ROLE', 'DEQUEUE ANY QUEUE', 'DROP ANY VIEW', 'CONTEXT', 'ALTER SESSION', 'DROP ANY SEQUENCE',
        'ALTER PUBLIC DATABASE LINK', 'GLOBAL QUERY REWRITE', 'DROP ANY MINING MODEL'
    )
    """

    cursor.execute(query2)
    results = cursor.fetchall()

    if not results:
        return "Done"
    else:
        missing_audit_options = [row[0] for row in results]
        print(missing_audit_options)
        return "Fail"


# V-15642
def check_v_15642(connection):
    cursor = connection.cursor()

    # Query to list sensitive data access controls
    query = """
    SELECT grantee, table_name, privilege 
    FROM dba_tab_privs
    WHERE table_name IN (
        SELECT table_name 
        FROM all_tables
        WHERE owner = 'SENSITIVE_SCHEMA' -- Replace with the schema containing sensitive data
    )
    """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return "Done"

    # Review the System Security Plan (SSP) requirements
    ssp_access_controls = {
        # Example format: ("USER_ROLE", "SENSITIVE_TABLE", "SELECT/INSERT/UPDATE/DELETE")
        ("AUTHORIZED_ROLE", "SENSITIVE_TABLE", "SELECT"),
        ("AUTHORIZED_ROLE", "SENSITIVE_TABLE", "UPDATE"),
        # Add more as per SSP
    }

    # Compare database grants with SSP
    findings = []
    for grantee, table_name, privilege in results:
        if (grantee, table_name, privilege) not in ssp_access_controls:
            findings.append((grantee, table_name, privilege))
            print((grantee, table_name, privilege))

    if not findings:
        return "Done"
    else:
        return "Fail"


# V-2539
def check_v_2539(connection):
    cursor = connection.cursor()

    # Query to check EXECUTE permissions for restricted Oracle packages granted to PUBLIC
    query = """
    SELECT table_name 
    FROM dba_tab_privs
    WHERE grantee = 'PUBLIC' 
    AND privilege = 'EXECUTE'
    AND table_name IN (
        'UTL_FILE', 'UTL_SMTP', 'UTL_TCP', 'UTL_HTTP',
        'DBMS_RANDOM', 'DBMS_LOB', 'DBMS_SQL',
        'DBMS_SYS_SQL', 'DBMS_JOB', 
        'DBMS_BACKUP_RESTORE', 
        'DBMS_OBFUSCATION_TOOLKIT'
    )
    """
    cursor.execute(query)
    results:list = cursor.fetchall()

    for item in [('DBMS_LOB',),('DBMS_SQL',),('DBMS_JOB',),('DBMS_OBFUSCATION_TOOLKIT',),('DBMS_RANDOM',)]:
        results.remove(item)

    if not results:
        return "Done"
    else:
        for row in results:
            print(row)
        return "Fail"



# V-15632:
def check_v_15632(connection):
    cursor = connection.cursor()
    query_dba_objects = r"""
    SELECT owner, object_name, object_type
    FROM dba_objects
    WHERE owner IN (
        SELECT grantee
        FROM dba_role_privs
        WHERE granted_role = 'DBA'
    )
    """
    cursor.execute(query_dba_objects)
    dba_objects = cursor.fetchall()
    for owner, object_name, object_type in dba_objects:
        query_non_dba_access = r"""
        SELECT grantee
        FROM dba_tab_privs
        WHERE owner = :owner
        AND table_name = :object_name
        AND grantee NOT IN (
            SELECT grantee
            FROM dba_role_privs
            WHERE granted_role = 'DBA'
        )

        """
        cursor.execute(query_non_dba_access, {'owner': owner, 'object_name': object_name})
        non_dba_access = cursor.fetchall()

        if non_dba_access:
            return "Fail"

    query_dba_docs = r"""
    SELECT COUNT(*)
    FROM dba_audit_trail
    WHERE action_name = 'READ DOCUMENTATION' -- Hypothetical action to log documentation access
    """
    cursor.execute(query_dba_docs)
    documentation_check = cursor.fetchone()

    if documentation_check[0] == 0:
        return "Fail"

    return "Done"


# V-15631:
def check_v_15631(connection):
    cursor = connection.cursor()
    query = r"""
    SELECT grantee, privilege, owner, table_name 
    FROM dba_tab_privs
    WHERE (owner='SYS' OR table_name LIKE 'DBA_%') 
      AND privilege <> 'EXECUTE'
      AND grantee NOT IN (
        'PUBLIC', 'AQ_ADMINISTRATOR_ROLE', 'AQ_USER_ROLE',
        'AURORA$JIS$UTILITY$', 'OSE$HTTP$ADMIN', 'TRACESVR',
        'CTXSYS', 'DBA', 'DELETE_CATALOG_ROLE',
        'EXECUTE_CATALOG_ROLE', 'EXP_FULL_DATABASE',
        'GATHER_SYSTEM_STATISTICS', 'HS_ADMIN_ROLE',
        'IMP_FULL_DATABASE', 'LOGSTDBY_ADMINISTRATOR', 'MDSYS',
        'ODM', 'OEM_MONITOR', 'OLAPSYS', 'ORDSYS', 'OUTLN',
        'RECOVERY_CATALOG_OWNER', 'SELECT_CATALOG_ROLE',
        'SNMPAGENT', 'SYSTEM', 'WKSYS', 'WKUSER', 'WMSYS',
        'WM_ADMIN_ROLE', 'XDB', 'LBACSYS', 'PERFSTAT', 'XDBADMIN'
      )
      AND grantee NOT IN (
        SELECT grantee FROM dba_role_privs WHERE granted_role='DBA'
      )
    ORDER BY grantee
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return "Fail" if result else "Done"


# V-15623:
def check_v_15623(connection):
    cursor = connection.cursor()
    query = r"""
    SELECT file_name 
    FROM dba_data_files 
    WHERE tablespace_name = 'SYSTEM'
    """
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return "Fail"

    directories = set(os.path.dirname(row[0]) for row in result)
    for directory in directories:
        try:
            files = os.listdir(directory)
            allowed_extensions = ('.dbf', '.log', '.ctl')
            for file in files:
                if not file.lower().endswith(allowed_extensions):
                    return "Fail"
        except Exception as e:
            print(f"Error accessing directory {directory}: {e}")
            return "Fail"

    return "Done"


# v-15626
def check_v_15626(connection):
    """
    Checks if database privileged role assignments are restricted to authorized accounts.
    Returns "Done" if all role assignments are to authorized accounts, "Fail" otherwise.
    """
    cursor = connection.cursor()
    try:
        # List of default/authorized Oracle accounts
        default_accounts = """
        'ANONYMOUS','AURORA$JIS$UTILITY$','AURORA$ORB$UNAUTHENTICATED','CTXSYS',
        'DBSNMP','DIP','DMSYS','DVF','DVSYS','EXFSYS','LBACSYS','MDDATA','MDSYS',
        'MGMT_VIEW','ODM','ODM_MTR','OLAPSYS','ORDPLUGINS','ORDSYS',
        'OSE$HTTP$ADMIN','OUTLN','PERFSTAT','REPADMIN','RMAN',
        'SI_INFORMTN_SCHEMA','SYS','SYSMAN','SYSTEM','TRACESVR',
        'TSMSYS','WK_TEST','WKPROXY','WKSYS','WKUSER','WMSYS','XDB'
        """

        # List of standard roles to exclude from check
        standard_roles = """
        'DBA','OLAP_USER','IP','ORASSO_PUBLIC','PORTAL_PUBLIC',
        'DATAPUMP_EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE',
        'EXP_FULL_DATABASE','IMP_FULL_DATABASE','OLAP_DBA',
        'EXECUTE_CATALOG_ROLE','SELECT_CATALOG_ROLE','JAVASYSPRIV',
        'CONNECT','RESOURCE','AUTHENTICATEDUSER'
        """

        # List of privileged roles to check
        privileged_roles = """
        'AQ_ADMINISTRATOR_ROLE','AQ_USER_ROLE','CTXAPP',
        'DELETE_CATALOG_ROLE','EJBCLIENT','EXECUTE_CATALOG_ROLE',
        'EXP_FULL_DATABASE','GATHER_SYSTEM_STATISTICS',
        'GLOBAL_AQ_USER_ROLE','HS_ADMIN_ROLE','IMP_FULL_DATABASE',
        'JAVADEBUGPRIV','JAVAIDPRIV','JAVASYSPRIV','JAVAUSERPRIV',
        'JAVA_ADMIN','JAVA_DEPLOY','LOGSTDBY_ADMINISTRATOR',
        'OEM_MONITOR','OLAP_DBA','RECOVERY_CATALOG_OWNER',
        'SALES_HISTORY_ROLE','SELECT_CATALOG_ROLE','WKUSER',
        'WM_ADMIN_ROLE','XDBADMIN'
        """

        query = f"""
        SELECT grantee, granted_role
        FROM dba_role_privs
        WHERE grantee NOT IN ({default_accounts})
        AND grantee NOT IN ({standard_roles})
        AND grantee NOT IN (SELECT grantee FROM dba_role_privs WHERE granted_role = 'DBA')
        AND grantee NOT IN (SELECT DISTINCT owner FROM dba_objects)
        AND granted_role IN ({privileged_roles})
        ORDER BY grantee
        """

        cursor.execute(query)
        unauthorized_grants = cursor.fetchall()

        if unauthorized_grants:
            # Log unauthorized role assignments for review
            print("Unauthorized privileged role assignments found:")
            for grantee, role in unauthorized_grants:
                print(f"Grantee: {grantee}, Role: {role}")
            return "Fail"

        return "Done"

    except cx_Oracle.DatabaseError as e:
        print(f"Error checking privileged role assignments (V-15626): {e}")
        return "Error"
    finally:
        cursor.close()



# v-15627
def check_v_15627(connection):
    """
    Verifies that administrative privileges are assigned to accounts via roles and not directly.
    """
    cursor = connection.cursor()
    try:
        # SQL query to identify accounts with directly assigned administrative privileges
        query = """
        SELECT grantee, privilege
        FROM dba_sys_privs
        WHERE grantee NOT IN
          ('SYS', 'SYSTEM', 'SYSMAN', 'CTXSYS', 'MDSYS', 'WKSYS')
          AND grantee NOT IN
          (
            SELECT DISTINCT granted_role
            FROM dba_role_privs
          )
          AND privilege <> 'UNLIMITED TABLESPACE'
        ORDER BY grantee
        """
        cursor.execute(query)
        unauthorized_privileges = cursor.fetchall()

        # If there are unauthorized privilege assignments, fail the check
        if unauthorized_privileges:
            print("Unauthorized direct administrative privilege assignments detected:")
            for grantee, privilege in unauthorized_privileges:
                print(f"Grantee: {grantee}, Privilege: {privilege}")
            return "Fail"

        # Otherwise, pass the check
        return "Done"
    except cx_Oracle.DatabaseError as e:
        # Handle unexpected database errors without disrupting compliance check flow
        print(f"Database error encountered: {e}")
        return "Fail"
    finally:
        cursor.close()



# v-15628
def check_v_15628(connection):
    """
    Verifies that DBMS application users are not granted administrative privileges (ALTER, REFERENCES, INDEX).
    """
    cursor = connection.cursor()
    try:
        # SQL query to check for administrative privileges assigned to application users
        query = """
        SELECT grantee, owner, table_name, privilege
        FROM dba_tab_privs
        WHERE privilege IN ('ALTER', 'REFERENCES', 'INDEX')
          AND grantee NOT IN ('DBA', 'SYS', 'SYSTEM', 'LBACSYS', 'XDBADMIN')
          AND table_name NOT IN ('SDO_IDX_TAB_SEQUENCE', 'XDB$ACL', 'XDB_ADMIN')
          AND grantee NOT IN (
            SELECT grantee
            FROM dba_role_privs
            WHERE granted_role = 'DBA'
          )
          AND grantee NOT IN (
            SELECT DISTINCT owner
            FROM dba_objects
          )
        """
        cursor.execute(query)
        unauthorized_privileges = cursor.fetchall()

        # If any unauthorized privileges are found, fail the check
        if unauthorized_privileges:
            print(
                "Unauthorized administrative privileges detected for application users:")
            for grantee, owner, table_name, privilege in unauthorized_privileges:
                print(f"Grantee: {grantee}, Owner: {owner}, Table: {
                      table_name}, Privilege: {privilege}")
            return "Fail"

        # Otherwise, pass the check
        return "Done"
    except cx_Oracle.DatabaseError as e:
        # Handle unexpected database errors without disrupting the flow
        print(f"Database error encountered: {e}")
        return "Fail"
    finally:
        cursor.close()


# V-15629
def check_v_15629(connection):
    """
    بررسی مجوزهای نامعتبر کاربران.
    """
    if connection is None:
        print("Connection not established.")
        return "Error"

    cursor = connection.cursor()
    query = """
    SELECT grantee || ': ' || privilege || ': ' || owner || '.' || table_name 
    FROM dba_tab_privs 
    WHERE grantee NOT IN (
        SELECT role FROM dba_roles
    )
    AND grantee NOT IN (
        'APEX_PUBLIC_USER', 'AURORA$JIS$UTILITY$', 'CTXSYS', 'DBSNMP', 'EXFSYS', 
        'FLOWS_030000', 'FLOWS_FILES', 'LBACSYS', 'MDSYS', 'MGMT_VIEW', 'ODM', 
        'OLAPSYS', 'ORACLE_OCM', 'ORDPLUGINS', 'ORDSYS', 'OSE$HTTP$ADMIN', 'OUTLN', 
        'OWBSYS', 'PERFSTAT', 'PUBLIC', 'REPADMIN', 'SYS', 'SYSMAN', 'SYSTEM', 
        'WKSYS', 'WMSYS', 'XDB'
    )
    AND table_name <> 'DBMS_REPCAT_INTERNAL_PACKAGE'
    AND table_name NOT LIKE '%RP'
    AND grantee NOT IN (
        SELECT grantee FROM dba_tab_privs WHERE table_name IN ('DBMS_DEFER', 'DEFLOB')
    )
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            return "Fail"
        else:
            return "Pass"

    except cx_Oracle.DatabaseError as e:
        print(f"Database error occurred: {e}")
        return "Fail"

    finally:
        if cursor:
            cursor.close()


# V-2508
def check_v_2508(connection):
    """
    بررسی وجود کاربران نامعتبر در پایگاه داده.
    """
    if not connection:
        print("Connection is not established.")
        return "Fail"

    cursor = None
    try:
        cursor = connection.cursor()
        query = "SELECT username FROM dba_users ORDER BY username"
        cursor.execute(query)
        results = cursor.fetchall()

        print("List of database users:")
        for record in results:
            print(record[0])

        print("\nCompare the above list with the authorized user list.")
        print("If any accounts listed are not clearly authorized, this is a Finding.")

        return "Fail" if results else "Pass"
    except cx_Oracle.DatabaseError as e:
        print(f"Database error occurred: {e}")
        return "Fail"
    finally:
        if cursor:
            cursor.close()


# V-15634
def check_v_15634(connection):
    """
    بررسی تنظیمات پروفایل‌های امنیتی.
    """
    try:
        cursor = connection.cursor()

        # Query 1: List all users
        print("Fetching all database users...")
        user_query = "SELECT username FROM dba_users ORDER BY username"
        cursor.execute(user_query)
        users = cursor.fetchall()
        print("\nList of database users:")
        for user in users:
            print(user[0])
        print("\nCompare this list with the authorized user list.")
        print("If any accounts listed are not clearly authorized, this is a finding.")

        # Query 2: Check profiles without PASSWORD_VERIFY_FUNCTION
        print("\nChecking profiles without PASSWORD_VERIFY_FUNCTION...")
        profile_query = """
        SELECT DISTINCT profile 
        FROM dba_profiles 
        WHERE resource_name = 'PASSWORD_VERIFY_FUNCTION' AND (limit IS NULL OR limit = 'NULL')
        """
        cursor.execute(profile_query)
        profiles_without_function = cursor.fetchall()
        if profiles_without_function:
            print("Profiles without PASSWORD_VERIFY_FUNCTION:")
            for profile in profiles_without_function:
                print(profile[0])
        else:
            print("All profiles have a PASSWORD_VERIFY_FUNCTION.")

        # Query 3: Check password-authenticated accounts
        print("\nChecking password-authenticated accounts...")
        password_accounts_query = "SELECT username FROM dba_users WHERE authentication_type = 'PASSWORD'"
        cursor.execute(password_accounts_query)
        password_accounts = cursor.fetchall()
        if password_accounts:
            print("Password-authenticated accounts:")
            for account in password_accounts:
                print(account[0])
        else:
            print("No password-authenticated accounts found.")

        return "Done"
    except cx_Oracle.DatabaseError as e:
        print(f"Error occurred during check_v_15634: {e}")
        return "Error"
    finally:
        if cursor:
            cursor.close()


# check_v_15141
def check_v_15141(connection):
    """
    Verifies that DBMS processes or services are running under custom, dedicated OS accounts.
    """
    system_type = platform.system().lower()

    if "linux" in system_type or "unix" in system_type:
        return check_unix_process_ownership()
    elif "windows" in system_type:
        return check_windows_service_ownership()
    else:
        return "Unsupported OS type for this check."


def check_unix_process_ownership():
    """
    Verifies process ownership for Oracle processes on UNIX-based systems.
    """
    try:
        # Commands to check Oracle processes
        processes = {
            "database": "ps -ef | grep -i pmon | grep -v grep",
            "listener": "ps -ef | grep -i tns | grep -v grep",
            "agent": "ps -ef | grep -i dbsnmp | grep -v grep",
        }

        findings = []

        for process_type, command in processes.items():
            result = subprocess.getoutput(command)
            if result:
                for line in result.strip().split("\n"):
                    parts = line.split()
                    owner = parts[0]  # The first column is the process owner
                    if owner != "oracle":  # Replace "oracle" with the expected dedicated account
                        findings.append(
                            f"{process_type} process not owned by 'oracle': {line}")
            else:
                findings.append(f"No {process_type} processes found.")

        if findings:
            print("Findings for UNIX-based systems:")
            for finding in findings:
                print(f"- {finding}")
            return "Fail"
        return "Done"
    except Exception as e:
        print(f"Error during UNIX process ownership check: {e}")
        return "Fail"


def check_windows_service_ownership():
    """
    Verifies service ownership for Oracle processes on Windows systems.
    """
    try:
        # Use PowerShell to retrieve Oracle services and their "Log On As" accounts
        command = [
            "powershell",
            "-Command",
            "Get-WmiObject Win32_Service | Where-Object {$_.Name -like 'Oracle*'} | Select-Object Name,StartName"
        ]
        result = subprocess.getoutput(command)
        findings = []

        for line in result.strip().split("\n"):
            if "Oracle" in line:
                parts = line.split()
                service_name = parts[0]
                start_name = " ".join(parts[1:])

                # Check if the service is running as LocalSystem
                if "LocalSystem" in start_name:
                    findings.append(
                        f"Service '{service_name}' is running as 'LocalSystem'.")
                elif "oracle" not in start_name.lower():
                    findings.append(f"Service '{
                                    service_name}' is not using a dedicated Oracle OS account: {start_name}")

        if findings:
            print("Findings for Windows systems:")
            for finding in findings:
                print(f"- {finding}")
            return "Fail"
        return "Done"
    except Exception as e:
        print(f"Error during Windows service ownership check: {e}")
        return "Fail"


# V-15654
def check_v_15654(connection):
    """
    Checks if symmetric keys are properly protected according to FIPS 140-2 standards
    and if Oracle Advanced Security is installed and operational.
    Returns "Done" if requirements are met, "Fail" otherwise.
    """
    cursor = connection.cursor()
    try:
        # Check if Oracle Advanced Security is installed and operational
        advanced_security_query = """
        SELECT PARAMETER, VALUE 
        FROM V$OPTION 
        WHERE PARAMETER = 'Advanced Security'
        """
        cursor.execute(advanced_security_query)
        advanced_security_result = cursor.fetchone()

        if not advanced_security_result or advanced_security_result[1] != 'TRUE':
            print("Oracle Advanced Security is not installed or not operational")
            return "Fail"

        # Check for the presence of symmetric keys
        symmetric_keys_query = """
        SELECT COUNT(*) 
        FROM V$ENCRYPTION_WALLET w, V$ENCRYPTION_KEYS k
        WHERE w.STATUS = 'OPEN'
        """

        try:
            cursor.execute(symmetric_keys_query)
            keys_count = cursor.fetchone()[0]

            if keys_count > 0:
                # If symmetric keys are present, verify encryption wallet status
                wallet_status_query = """
                SELECT STATUS, WALLET_TYPE 
                FROM V$ENCRYPTION_WALLET
                """
                cursor.execute(wallet_status_query)
                wallet_status = cursor.fetchone()

                if not wallet_status or wallet_status[0] != 'OPEN':
                    print("Encryption wallet is not properly configured or not open")
                    return "Fail"

                # Check TDE (Transparent Data Encryption) configuration
                tde_query = """
                SELECT PARAMETER, VALUE 
                FROM V$SYSTEM_PARAMETER 
                WHERE PARAMETER = 'ENCRYPTION_WALLET_LOCATION'
                """
                cursor.execute(tde_query)
                tde_config = cursor.fetchone()

                if not tde_config or not tde_config[1]:
                    print("TDE wallet location is not properly configured")
                    return "Fail"

            # Additional checks that would normally require manual verification:
            print("Manual verification required for:")
            print("1. Key management procedures in System Security Plan")
            print("2. Evidence of procedure compliance in audit logs")
            print("3. Key lifecycle management documentation")
            print("4. Key backup and recovery procedures")
            print("5. Key rotation schedules")

            return "Done"

        except cx_Oracle.DatabaseError:
            print("Unable to verify symmetric key configuration - check permissions")
            return "Fail"

    except cx_Oracle.DatabaseError as e:
        print(f"Error checking symmetric key management (V-15654): {e}")
        return "Error"
    finally:
        cursor.close()


def get_encryption_algorithms(connection):
    """
    Helper function to get the list of encryption algorithms in use.
    """
    cursor = connection.cursor()
    try:
        query = """
        SELECT DISTINCT ENCRYPTION_ALG 
        FROM V$ENCRYPTED_TABLESPACES 
        UNION 
        SELECT DISTINCT ENCRYPTION_ALG 
        FROM V$ENCRYPTED_TABLES
        """
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except cx_Oracle.DatabaseError as e:
        print(f"Error retrieving encryption algorithms: {e}")
        return []
    finally:
        cursor.close()


# v-15657
def check_v_15657(connection):
    """
    Checks if changes to DBMS security labels are properly audited.
    Returns "Done" if audit requirements are met, "Fail" if not, and "Not Applicable"
    if security labeling is not required.
    """
    cursor = connection.cursor()
    try:
        # First check if Oracle Label Security is installed
        ols_check_query = """
        SELECT PARAMETER, VALUE 
        FROM V$OPTION 
        WHERE PARAMETER = 'Oracle Label Security'
        """
        cursor.execute(ols_check_query)
        ols_result = cursor.fetchone()

        if not ols_result or ols_result[1] != 'TRUE':
            print("Oracle Label Security is not installed")
            return "Fail"

        # Check if any OLS policies exist
        policy_check_query = """
        SELECT POLICY_NAME 
        FROM DBA_SA_POLICIES
        """
        try:
            cursor.execute(policy_check_query)
            policies = cursor.fetchall()

            if not policies:
                print("No Oracle Label Security policies found")
                return "Not Applicable"

            # Check audit settings for existing policies
            audit_check_query = """
            SELECT * FROM DBA_SA_AUDIT_OPTIONS
            """
            cursor.execute(audit_check_query)
            audit_settings = cursor.fetchall()

            if not audit_settings:
                print("No audit settings found for security labels")
                return "Fail"

            # Check specific audit options that should be enabled
            required_audit_options = [
                'POLICY_ADMIN',        # Auditing of policy administrative operations
                'SET_LABELS',          # Auditing of label modifications
                'LEVEL_CHANGES',       # Auditing of security level changes
                'COMPARTMENT_CHANGES',  # Auditing of compartment changes
                'GROUP_CHANGES'        # Auditing of group changes
            ]

            missing_audits = []
            for option in required_audit_options:
                found = False
                for setting in audit_settings:
                    if option in str(setting):
                        found = True
                        break
                if not found:
                    missing_audits.append(option)

            if missing_audits:
                print("Missing required audit options:")
                for option in missing_audits:
                    print(f"- {option}")
                return "Fail"

            return "Done"

        except cx_Oracle.DatabaseError:
            print("Unable to verify OLS audit settings - check permissions")
            return "Error"

    except cx_Oracle.DatabaseError as e:
        print(f"Error checking security label auditing (V-15657): {e}")
        return "Error"
    finally:
        cursor.close()


def get_ols_policies(connection):
    """
    Helper function to get the list of Oracle Label Security policies.
    """
    cursor = connection.cursor()
    try:
        query = """
        SELECT POLICY_NAME, POLICY_OPTIONS 
        FROM DBA_SA_POLICIES
        """
        cursor.execute(query)
        return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        print(f"Error retrieving OLS policies: {e}")
        return []
    finally:
        cursor.close()


# Saving results
def save_results(df, results):
    for code, result in results.items():
        df.loc[df["id"] == code, "Result"] = result
    df.to_excel(file_path, index=False)
    print("Results updated in the file.")

# تابع اصلی
def main():
    df = pd.read_excel(file_path)
    connection = connect_to_oracle()


    try:
        results = {
            "V-2554": check_v_2554(connection),
            "V-2555": check_v_2555(connection),
            "V-15635": check_v_15635(connection),
            "V-3810": check_v_3810(connection),
            "V-16033": check_v_16033(connection),
            "V-3817": check_v_3817(connection),
            "V-3815": check_v_3815(connection),
            "V-15637": check_v_15637(connection),
            "V-15633": check_v_15633(connection),
            "V-2558": check_v_2558(connection),
            "V-15639": check_v_15639(connection),
            "V-15634": check_v_15634(connection),
            "V-15613": check_v_15613(connection),
            "V-2520": check_v_2520(connection),
            "V-2527": check_v_2527(connection),
            "V-15615": check_v_15615(connection),
            "V-2516": check_v_2516(connection),
            "V-2593": check_v_2593(connection),
            "V-15152": check_v_15152(connection),
            "V-15153": check_v_15153(connection),
            "V-2424": check_v_2424(connection),
            "V-3818": check_v_3818(connection),
            "V-15644": check_v_15644(connection),
            "V-15642": check_v_15642(connection),
            "V-2539": check_v_2539(connection),
            "V-15632": check_v_15632(connection),
            "V-15631": check_v_15631(connection),
            "V-15623": check_v_15623(connection),
            "V-15626": check_v_15626(connection),
            "V-15627": check_v_15627(connection),
            "V-15628": check_v_15628(connection),
            "V-15629": check_v_15629(connection),
            "V-2508": check_v_2508(connection),
            "V-15141": check_v_15141(connection),
            "V-15654": check_v_15654(connection),
            "V-15657": check_v_15657(connection)
        }
        save_results(df, results)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
