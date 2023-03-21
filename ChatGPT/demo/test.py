import flask, json
from flask import request
from revChatGPT.revChatGPT import Chatbot
config = {
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..gw09R5LEIPpkzyGW.upEFR_r9Eiom6fsB-UNOaF8Lhjk8itRhYntSWUgrWiikRHYaOxYh6po-YvJ2tXtVG-bZ2xVaWQeQ4RNOHgdFazBS17B_zEGIFz7KpIvuZoSvLJmZccxzlMs-qrlXfwANVbtuSdj5kANxQbAqgjInEffGGlStoFw_CwQKAu1tnJH_PSO_JtgKVzG5j9Q7kMjQIJj3G-3Dk4ZM1GSoC_Ok7OUgbX53ND-mNALI4uHamLhgwOHFRwM15mfRWNEQwnSnnBwVogEXNk9x5osykpsHbbNXFCVzTCYPVFG7s1NfwTZ1o09rPz99JOxX392a7kZaJZ0shTXCjFmcFW3Ou9_3_l3VDVoclH3koOTZyVvzAd23lt5gEVqAxtijPBrULdYlu4mAf3uxiUnhIWhiMpOaeHUk1Q6tMiPMH_xud50uXdfiSW7ESB_Z13wOdlJFZVIpcrKn0c798oY5fPE4dxnRA-L_8rEo84Q95lHs43omyn8eAT58tXiKxtBYHJUB0o68NkUd6dC40ZS9BvDmWjFJBpxvagrr6xZ_Bl3RY0v5ALhilheMqEeqiRCMRiRhvdevFV7q1GJSKQpLLNuxpbR6fAq5dUDexeEHVSKgjD8NxfcjkqvPVaf1klwyS6T1UAfT8nsJoxQOG_Ni-etNRmbqJXGUYHHmREr8mKObDXkqmcI5RpbNSFsFj9cNACJXfByonCdpQOVi7KgdH3acYdeTbTgth_rqfoWvQeXCEZyEDzSurFuRDmdM6FAoEpLHsH-4EHH3TNmFUxHh2L8FxnLssfzoxnE4x2QFLXRCLrNvRIfKjXCiVImTao4D31PvO8yyB4yy8fsoT8qjdMgo4WmeK-d2F4_BbEoKQ9C_mi1X6oydh6vfHWrwqNil7qAw2xZYbl62powQ5lGIN55U-NQg_5PTmkgyRHE6XVqapqc2_wWUNxkTVk8kHcKzJ0pGYTCzDkRsbsiUIOe39_NKO0a-xvEdAkYP59Uv1PztSTaaPcBgkPhDHPQ_LvSQ0Tqd2XkYv2QF-b_dmzE1qgAxQV_HeBB_UHhuhkbBIS_fUeVIobgdJ-HstyY0qY7OlSeR891uPDSInEyOEBWEl-V-xzt8UIFZowmIs8R85RJsDuzGNJz_C6fCPhE86qG0HSsZAbwmrQYBZGDVY9c_OzaUyK5TNL_2d7meepie3i8sFzU7tDVrYSOSTCKnqgfx33iwviQv2T9wFIlhr7tYtajLBv9uKJp1exn3e4Rx1uJ5Fr8t4PuFvfneD0s8eQfKjFbuGRK8fySmj4lCFT0lylecAnDuFJKhWkPI0al-Q3RPJXbZ6Suko0U9xI5LLiwIberZXhvTHf_Zc19WEN2CVr8kfb6qYigMwzSGQvl1WtVwcYi9pZgvjrUd0QklFRgB76DIeCML2nVsMMPI_rMZ06S_YfEKaw6uzIOzHPzNuw5DaZzPevkC865RpBFiA8Icww-SUhC0YXy8OUnYQD9jE39hr7V5ohgMfxt0Sb4GqxXcU9J418eBxj3CFCU_R_ERRGJIjNKVFNzJtpFPhQyI60HWxIp2MI6lWV5cr8tf0KXwuAi1jltyIfM6rcAwHHge26XYHPgne6H8BFZDRo9-bBfNgucxlDllBg0zy8PHeJxog3t-KTkRc_2QaqnExxJRjLQllLvYW7-JNjxZxgVCLWQcvMizu0xiJigVS1K2LzUEr40WnXZUIWfmIIOSWD8vGzTUOE6RiAFZywF__ckHqCU9QkX07WCL7foxyM4u5_jQ4TzeR0NMJKx03cxNr9Eh-amT3y1p5qf_FuC3WT3OGYHAWdSBctoSM5unxl2T6WhH9MoqKKx0JrkmVo_8byHxxxz7nlChO6eXwzgI20NRGfoL0TXO5CkIwcA1BeoCzlJvSeTK75s_LtZRuY-hBAawgj_hnD1yeby_B5nEyCmA60ZnsM2veokjhX9cTTFzH2-eWfpsUTqjeygw9ErbM9hF89PUBdr5ptX5rCkbIZtty7lRgFubPH-6ZmKuza7roqR5jRuqqb-qQNDnSlmHRLvpyxzAs6Vz1lcjr68l4vJCXTnh98QetaIf6HHZuycGCmIzsEuJf7Fx6RFxtJqgQEi4R1_ucPOeQXVhckXiVhb9zI_Q_piWVHMEJX7jxCxA8Tb8R625-0YhxAKalT_VZi0RpntqeVUDVg0_KF77huqzpe2vH8J73aRLQmHMMS0b2sCzg6rosXoT4WXcuiba6toryvg-xRzz4UnyAVjJamMEa9RWv5Lr23ek2N4fIcIOMdInezrDsI-FIOqqtzjTHrhYudNTcYYW_Dn8pmRxJ2Dah9jc8yfnlDyXS6bYqEmbTIuQp95JTw.xKIhnubIx6pRHUSOayyCSg"
}
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)
chatbot = Chatbot(config)
def chat(msg):
    message = chatbot.get_chat_response(msg)['message']
    print(message)
    return message
# print(chat("你会数学吗？"))
@server.route('/chat', methods=['post'])
def chatapi():
    requestJson = request.get_data()
    if requestJson is None or requestJson == "" or requestJson == {}:
        resu = {'code': 1, 'msg': '请求内容不能为空'}
        return json.dumps(resu, ensure_ascii=False)
    data = json.loads(requestJson)
    print(data)
    try:
        msg = chat(data['msg'])
    except Exception as error:
        print("接口报错")
        resu = {'code': 1, 'msg': '请求异常: ' + str(error)}
        return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 0, 'data': msg}
        return json.dumps(resu, ensure_ascii=False)
if __name__ == '__main__':
    server.run(port=7777, host='0.0.0.0')