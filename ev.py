import os
class EV:
    HASURA_URL = os.getenv("url", "https://staging.admin.vip.voyceglobal.com/auth/login")
    url = 'https://staging.admin.vip.voyceglobal.com/auth/login'
    url1 = 'https://staging.vip.voyceglobal.com/auth/login'
    url_Kanji = 'https://voyce.kandji.io/signin'
    my_accaunt = "nikita.barshchuk@voyceglobal.com"
    my_accaunt_m = "nikita.barshchuk@equitihealth.com"
    my_password = os.getenv('my_password')
    my_password1 = os.getenv('my_password1')
    deafult_password = os.getenv('deafult_password')
    CLIENT_ID = os.getenv('CLIENT_ID')
    PROJECT_ID =os.getenv('PROJECT_ID')
    AUTH_URI = os.getenv('AUTH_URI')
    TOKEN_URI = os.getenv('TOKEN_URI')
    AUTH_PROVIDER_CERT_URL = os.getenv('AUTH_PROVIDER_CERT_URL')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI =os.getenv('REDIRECT_URI')
    TOKEN = os.getenv('TOKEN')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
    TOKEN_URI = os.getenv('TOKEN_URI')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = os.getenv('SCOPES')
    EXPIRY = os.getenv('EXPIRY')
    
    


    
    my_accaunt_wd = "nikita.barshchuk"
    
    login_qa_hud = "nikita.qa"
    wei_p = os.getenv('wei_p')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

    email_list_for_acc_creation = [
        'adam1.worman@voyceglobal.com', 'adriana1.quintero@voyceglobal.com', 'aldo1.lorenzo@voyceglobal.com',
        'ana1.maria.mejia@voyceglobal.com', 'aurelio1.adames@voyceglobal.com', 'autumn1.adams@voyceglobal.com',
        'axelle1.augustin@voyceglobal.com', 'byron1.miller@voyceglobal.com', 'carlos1.alvarado@voyceglobal.com',
        'carrie1.chen@voyceglobal.com', 'cecilia1.baqueiro@voyceglobal.com',
        'christian1.cantabrana@voyceglobal.com',
        'christian1.gloverwilson@voyceglobal.com', 'claudia1.altamirano@voyceglobal.com',
        'dania1.juarez@voyceglobal.com',
        'daniel1.pirestani@voyceglobal.com', 'daniela1.rodriguez@voyceglobal.com', 'debela1.chali@voyceglobal.com',
        'ehno1.paw@voyceglobal.com', 'elizabeth1.rosas@voyceglobal.com',
        'elzebir1.delcid@voyceglobal.com', 'ghada1.mohsen@voyceglobal.com', 'gloria1.alvarez@voyceglobal.com',
        'jean1.sarlat@voyceglobal.com', 'jeremy1.waiser@voyceglobal.com',
        'jessica1.pollock@voyceglobal.com', 'jonathan1.scott@voyceglobal.com', 'juan1.carrillo@voyceglobal.com',
        'kevin1.sillas@voyceglobal.com', 'laura1.keylon@voyceglobal.com', 'leidy1.ocampo@voyceglobal.com',
        'maria1.belen@voyceglobal.com', 'maria1.jalil@voyceglobal.com', 'maria1.rivera@voyceglobal.com',
        'marianne1.bustamante@voyceglobal.com', 'martin1.cedeno@voyceglobal.com', 'matthew1.dong@voyceglobal.com',
        'mauricio1.iragorri@voyceglobal.com', 'mayra1.morante@voyceglobal.com', 'mesac1.cleus@voyceglobal.com',
        'monitordisplay1.@weyimobile.com', 'naing1.ayar@voyceglobal.com', 'natalia1.schell@voyceglobal.com',
        'ning1.hu@voyceglobal.com', 'okon1.gordon@voyceglobal.com', 'olga1.bedoya@voyceglobal.com',
        'pascal1.concepcion@voyceglobal.com', 'patrick1.faroul@voyceglobal.com', 'paula1.cassiano@voyceglobal.com',
        'qa1.tester@voyceglobal.com', 'rich1.forbes@voyceglobal.com', 'ryma1.chowdhury@voyceglobal.com',
        'sahar1.eslami@voyceglobal.com', 'sheila1.lou@voyceglobal.com', 'sthefani1.rodriguez@voyceglobal.com',
        'tara1.mocco@voyceglobal.com', 'taylor1.mcdermott@voyceglobal.com', 'terry1.quintero@voyceglobal.com',
        'valentina1.ardila@voyceglobal.com', 'wli1.@weyimobile.com', 'xiang1.@weyimobile.com',
        'yesenia1.pirestani@voyceglobal.com', 'yoshelinne1.monroy@voyceglobal.com',
        'jhadir1.mendoza@voyceglobal.com',
        'engels1.chavarria@voyceglobal.com'
    ]


    users = [
        {'Email': 'adam1.worman@voyceglobal.com'},
        {'Email': 'adriana1.quintero@voyceglobal.com'},
        {'Email': 'aldo1.lorenzo@voyceglobal.com'},
        {'Email': 'ana1.maria.mejia@voyceglobal.com'},
        {'Email': 'aurelio1.adames@voyceglobal.com'},
        {'Email': 'autumn1.adams@voyceglobal.com'},
        {'Email': 'axelle1.augustin@voyceglobal.com'},
        {'Email': 'byron1.miller@voyceglobal.com'},
        {'Email': 'carlos1.alvarado@voyceglobal.com'},
        {'Email': 'carrie1.chen@voyceglobal.com'},
        {'Email': 'cecilia1.baqueiro@voyceglobal.com'},
        {'Email': 'christian1.cantabrana@voyceglobal.com'},
        {'Email': 'juan.carrillo@voyceglobal.com'},
        {'Email': 'claudia1.altamirano@voyceglobal.com'},
        {'Email': 'dania1.juarez@voyceglobal.com'},
        {'Email': 'daniel1.pirestani@voyceglobal.com'},
        {'Email': 'daniela1.rodriguez@voyceglobal.com'},
        {'Email': 'debela1.chali@voyceglobal.com'},
        {'Email': 'ehno1.paw@voyceglobal.com'},
        {'Email': 'elizabeth1.rosas@voyceglobal.com'},
        {'Email': 'elzebir1.delcid@voyceglobal.com'},
        {'Email': 'ghada1.mohsen@voyceglobal.com'},
        {'Email': 'gloria1.alvarez@voyceglobal.com'},
        {'Email': 'jean1.sarlat@voyceglobal.com'},
        {'Email': 'jeremy1.waiser@voyceglobal.com'},
        {'Email': 'jessica1.pollock@voyceglobal.com'},
        {'Email': 'jonathan1.scott@voyceglobal.com'},
        {'Email': 'juan1.carrillo@voyceglobal.com'},
        {'Email': 'adam.worman@voyceglobal.com'},
        {'Email': 'adriana.quintero@voyceglobal.com'},
        {'Email': 'aldo.lorenzo@voyceglobal.com'},
        {'Email': 'ana.maria.mejia@voyceglobal.com'},
        {'Email': 'aurelio.adames@voyceglobal.com'},
        {'Email': 'autumn.adams@voyceglobal.com'},
        {'Email': 'axelle.augustin@voyceglobal.com'},
        {'Email': 'byron.miller@voyceglobal.com'},
        {'Email': 'carlos.alvarado@voyceglobal.com'},
        {'Email': 'carrie.chen@voyceglobal.com'},
        {'Email': 'cecilia.baqueiro@voyceglobal.com'},
        {'Email': 'christian.cantabrana@voyceglobal.com'},
        {'Email': 'maria1.rivera@voyceglobal.com'},
        {'Email': 'claudia.altamirano@voyceglobal.com'},
        {'Email': 'dania.juarez@voyceglobal.com'},
        {'Email': 'daniel.pirestani@voyceglobal.com'},
        {'Email': 'daniela.rodriguez@voyceglobal.com'},
        {'Email': 'debela.chali@voyceglobal.com'},
        {'Email': 'ehno.paw@voyceglobal.com'},
        {'Email': 'kevin.sillas@voyceglobal.com'},
        {'Email': 'martin1.cedeno@voyceglobal.com'},
        {'Email': 'matthew1.dong@voyceglobal.com'},
        {'Email': 'mauricio1.iragorri@voyceglobal.com'},
        {'Email': 'mayra1.morante@voyceglobal.com'},
        {'Email': 'mesac1.cleus@voyceglobal.com'},
        {'Email': 'monitordisplay1.@weyimobile.com'},
        {'Email': 'naing1.ayar@voyceglobal.com'},
        {'Email': 'natalia1.schell@voyceglobal.com'},
        {'Email': 'ning1.hu@voyceglobal.com'},
        {'Email': 'okon1.gordon@voyceglobal.com'},
        {'Email': 'olga1.bedoya@voyceglobal.com'},
        {'Email': 'pascal1.concepcion@voyceglobal.com'},
        {'Email': 'patrick1.faroul@voyceglobal.com'},
        {'Email': 'paula1.cassiano@voyceglobal.com'},
        {'Email': 'christian1.gloverwilson@voyceglobal.com'},
        {'Email': 'kevin1.sillas@voyceglobal.com'},
        {'Email': 'laura1.keylon@voyceglobal.com'},
        {'Email': 'leidy1.ocampo@voyceglobal.com'},
        {'Email': 'maria1.belen@voyceglobal.com'},
        {'Email': 'maria1.jalil@voyceglobal.com'},
        {'Email': 'marianne1.bustamante@voyceglobal.com'}
    ]

    emails = [
        "tknapp@cac-sc.org",
        "alicia.barlow@ascension.org",
        "Cortiz@sunriver.org",
        "ebizoni@sunriver.org",
        "sseth@chla.usc.edu",
        "Mary.DaSilva@hcmed.org",
        "Jennifer.Viteri@nm.org",
        "CriscianeTran@llu.edu",
        "jacque.wilson@uhkc.org",
        "Carlos.Vargas@uhkc.org",
        "Megaan.Lorenzen@unchealth.unc.edu",
        "kpatton1@smcgov.org",
        "guadalupe.garcia@cookcountyhealth.org",
        "Kristen.Hadden@athletico.com",
        "brian.kelly@athletico.com",
        "soraya.silva@unchealth.unc.edu",
        "Gregory_Dillenbeck@whhs.com",
        "Brian_Smith@whhs.com",
        "Gisela_Hernandez@whhs.com",
        "Sara.Sellers@franciscanalliance.org",
        "lwilson@dccca.org",
        "Grace.Rey@leonmedicalcenters.com",
        "onyria.rojas@leonmedicalcenters.com",
        "erivera@tap360health.org",
        "vince_ly@whhs.com",
        "kelly.stanczak@athletico.com",
        "patricia.herford@atheltico.com",
        "matthew.cox@franciscanalliance.org",
        "kristofor.copes@franciscanalliance.org",
        "scott.cummings@nextalk.com",
        "VTadic@bruyere.org",
        "RobinGordon@texashealth.org",
        "PratibhaBhamoo@texashealth.org",
        "mcoreas@chla.usc.edu",
        "azaki@chla.usc.edu",
        "jason.cargile@midlandhealth.org",
        "elsa.reed@midlandhealth.org",
        "nancy.hill@midlandhealth.org",
        "fsfleur@huhosp.org",
        "brenda.busby@prismahealth.org",
        "PattersonJ@dvch.org",
        "tesparza@shieldsforfamilies.org",
        "Berenice.Ocampo-Guzman@nhcare.org",
        "rmartin@smcgov.org",
        "parana@smcgov.org",
        "James.Roxburgh@veeonehealth.com",
        "danielle.rich@veeonehealth.com",
        "Brigitte.Marcotte.ccomtl@ssss.gouv.qc.ca",
        "florita.de.jesus.vazquez@ascension.org",
        "julie@tstcc.ca",
        "amnixon@premierhealth.com",
        "jlefebvre@stridestoronto.ca",
        "jonathan.rios@anmed.org",
        "Danny.Alvarado@centralcityhealth.org",
        "rowena.manzano@centralcityhealth.org",
        "denise.nichols@nm.org",
        "garrett.knickerbocker@ascension.org",
        "Miannaci@nhcc.us",
        "levans@kooth.com",
        "JBullard@sls-health.com",
        "naman.shah@stridestoronto.ca",
        "sgifford@thebabyfold.org",
        "twilson@thebbyfold.org",
        "jlregister@thebabyfold.org",
        "vincent.gallagher@eskenazihealth.edu",
        "Meredith.Netzel@eskenazihealth.edu",
        "Maria.Jordan@eskenazihealth.edu",
        "N.Price@hhsil.com",
        "matt.sedgwick@rightsitehealth.com",
        "tlascar@mcsssd.us",
        "ktaylor@mcsssd.us",
        "Diana.Salinas@leonmedicalcenters.com",
        "Alessa.Ramos@snch.org",
        "rchan@kkv.net",
        "csimmons@kkv.net",
        "dderauf@kkv.net",
        "mkong@kkv.net",
        "minada@kkv.net",
        "jwatson@hfchc.net",
        "mcarter@ricemedicalcenter.net",
        "ruthie@completehumanco.com",
        "matthew.Post@bmcjax.com",
        "Lina.Hoyos@snch.org",
        "Amin.El-rowmeim@nyulangone.org",
        "Alim.Merchant@nyulangone.org",
        "Jonathan.Feldman@nyulangone.org",
        "irism@arizonaeyeconsultants.com",
        "ira.frenkel@chsli.org",
        "Gail.Mazza@chsli.org",
        "Jaime.Bray@towerhealth.org",
        "Claire.Alminde@towerhealth.org",
        "skhan@shn.ca",
        "negron-elizabeth@cooperhealth.edu",
        "jproffett@washosc.com",
        "arenaud@washosc.com",
        "OchoaA@archildrens.org",
        "jadamji@tap360health.org",
        "jellingwood@tap360health.org",
        "asudduth@wkhs.com",
        "tmann@wkhs.com",
        "rspringer@wkhs.com",
        "integrativewellnessms@gmail.com",
        "Kirstie.Matzek@shawneehealthcare.org",
        "cilam_gorkem@holyokehealth.com",
        "AFerrerMellor@valleychildrens.org",
        "Crystal.Jeter-Prince@ynhh.org",
        "Selena.Cardoso@bpthosp.org",
        "Debi.D'Alba@greenwichhospital.org",
        "Carlos.Aguero@LMHOSP.ORG",
        "Dorie.Gemmell@bpthosp.org",
        "Mohamed.MohamedHegazi@YNHH.ORG",
        "eimasa@primehealthcare.com",
        "nwasieczko@ecmc.edu",
        "lstoll@pediatrust.com",
        "jswartzlander@pediatrust.com",
        "greenfogel-vivian@cooperhealth.edu",
        "Scisorek-kevin@cooperhealth.edu",
        "viyee@oakvalleyhealth.ca",
        "dscanlon@ehs.org",
        "DietrichJ@childrensdayton.org",
        "ModdemanM@childrensdayton.org",
        "GeisJ@childrensdayton.org",
        "DennisS@myprimaryhealthsolutions.org",
        "dsmith@vlpp.org",
        "Steve@platinumcaremanagement.com",
        "GBarr@valleychildrens.org",
        "emejia@wayfinderfamily.org",
        "nds003@lvc.edu",
        "lcecil@ptcky.com",
        "jhubbard.wccindy@gmail.com",
        "cindyc@myprimaryhealthsolutions.org",
        "lance.fenton@nchmd.org",
        "robert.sweeney@emoryhealthcare.org",
        "beth.ryther@tiftregional.com",
        "ewest@jhchc.org",
        "Gabrielle@aslservices.com",
        "kmuhr@pchcares.org",
        "steve.lantz@tmmc.com",
        "Marjan.Bazleh@sinaihealth.ca",
        "Agnes.Tong@sinaihealth.ca",
        "natan@conduithealth.com",
        "horacio.ferreira@ascension.org",
        "carclant@witham.org",
        "al.faul@kennedychc.org",
        "Carlos_Olvera@rush.edu",
        "Sandra.Couto@unityhealth.to",
        "khehman@avinawomenscare.com",
        "Sara.Smith@kidshelpphone.ca",
        "helene.oleary@atlanticare.org",
        "demetrius.dillard@aspireindiana.org",
        "shill@enpcn.com",
        "admin@cmoh.ca",
        "dayna.setzkorn@contacthamilton.ca",
        "Shubham@receptionhouse.ca",
        "davisr@mcmsnj.net",
        "Wanda.Stephens@solismammo.com",
        "catinch@premierhealth.com",
        "Alden.Leung@bchsys.org",
        "tl@nestcollaborative.com",
        "mandi.bordelon@nestcollaborative.com",
        "runklecarol@gmail.com",
        "gabriella.gardner@uhkc.org",
        "alicia.lorenz@sih.net",
        "MCORBIN@haltonhealthcare.com",
        "slgehlha@purdue.edu",
        "dforres@siue.edu",
        "tduke@clintonpublicschools.com",
        "kathy.burgess@burgessprimary.com",
        "mpickel@brigidcollins.org",
        "jelliott@dsoser.com",
        "vonda.richey@fspcares.org",
        "jfavela@kcmh.net",
        "morgan.christensen@mosaicinfo.org",
        "rthomasjr@handsonny.com",
        "jsettoon@pchhh.org",
        "jeff@belaray.com",
        "michelle.gilbert@pufctrussville.com",
        "jordan.harris@purlifemedical.com",
        "drpeterson@drlullaby.com",
        "carrollcountydentalassociates@gmail.com",
        "jtucker@cibd-ca.org",
        "lsylvester@ascy.ca",
        "raymond.elwood@hdgh.org",
        "nicole.crozier@hdgh.org",
        "alison.murray@hdgh.org",
        "BDooley@atlanticare.org",
        "JSCOOPER@atlanticare.org",
        "WMikhail@llu.edu",
        "heatherm@jchdonline.org",
        "raji@theworldbridge.ca",
        "JVenegas@afcurgentcare.com",
        "Abby.Rinerson@mvpc.com",
        "Jessica.Satterfield@acadiahealthcare.com",
        "kpasma@sandyhillchc.on.ca",
        "stephanie@marketstreetdermatology.com",
        "dee@coloradoars.com",
        "SHerrin-Huneycutt@lscarolinas.net",
        "dtascoe@agapesway.com",
        "gabriella.gardner@uhkc.org",
        "RReyes@bethanychildrens.org",
        "mkaefer@sapublicschools.com",
        "cjharris@hinet.org",
        "apresha@valleyhealthlink.com",
        "rballard@peoriacounty.org",
        "shampshire@stclairchild.ca",
        "danny.mills@doxy.me",
        "wardc@woodbinefht.ca",
        "amber.brown@peterboroughfht.com",
        "CVernon@southlake.ca",
        "brshafer@med.umich.edu",
        "tmcpherson@harlemunited.org",
        "smccann@bryaneyes.com",
        "dana.wilson@aplushealth.org",
        "yvonne@westgateskin.com",
        "ljones@cmhahkpr.ca",
        "gabrielan@centurymedicaldental.com",
        "calkire@afcak.com",
        "k.baque@advancedtelemedicinegroupllc.com",
        "sdianat@dandelionhealth.com",
        "nelardo@fxphysicaltherapy.com",
        "hpha745@gmail.com",
        "mkaefer@sapublicschools.com",
        "ETeske@stanfordhealthcare.org",
        "laurie@painsanantonio.com",
        "kjones@sandyhillchc.on.ca"
    ]

    authorization_new_york33 = os.getenv('authorization_new_york33')
    authorization_check_company = os.getenv('authorization_check_company')
    authorization_EST = os.getenv('authorization_EST')
    authorization_Yale = os.getenv('authorization_Yale')
    authorization_for_widjets = os.getenv('authorization_for_widjets')
    authorization = os.getenv('authorization')
    new_password = os.getenv('new_password')

    role_check_desc = os.getenv('role_check_desc')
    mongo_client = os.getenv('mongo_client')
    mongo_client1 = os.getenv('mongo_client1')
    host = os.getenv('host')
    http = os.getenv('http')
    access_token = os.getenv('access_token')
    catalog = os.getenv('catalog')
    SSL = '/usr/local/etc/openssl@3/cert.pem'
    os = '/usr/local/etc/openssl@3/cert.pem'


