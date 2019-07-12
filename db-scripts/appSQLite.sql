PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('44e8b4031ccf');
CREATE TABLE admin (
	id INTEGER NOT NULL, 
	nickname VARCHAR(64), 
	email VARCHAR(120), 
	password_hash VARCHAR(128), 
	timestamp DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO "admin" VALUES(1,'compadmin','admin@localhost','$6$rounds=656000$3bP2.doJoQbi4JBi$SftaJWRdM8crEFjVcZ2Oa7GmpoHOQsRQuWLPO2JMyaUti8UhuYM9LOO2GSWoLUVpy9prcoleqVY.K.rC8okVG0','2017-11-27 22:16:47.487876');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(64), 
	timestamp DATETIME, 
	admin_id INTEGER, 
	description VARCHAR(100), 
	password_hash VARCHAR(128), 
	PRIMARY KEY (id), 
	FOREIGN KEY(admin_id) REFERENCES admin (id)
);
INSERT INTO "user" VALUES(1,'user1','2017-11-28 15:26:05.633647',1,'I''m the first user','$6$rounds=656000$sADvFzasi4JFiVcf$R1WF6HEi4aKxnVFP1bDhSyFcCHPD0APGFIO/3wJRpSR7BZXEWom9F9aS/J9YlGb51zbolDZXK8/NIde55TAbT.');
INSERT INTO "user" VALUES(2,'user2','2017-11-28 18:57:08.673049',1,'Another user','$6$rounds=656000$SlkqnLPv2M1dvLpC$kE9Sm7wQ6iphPoW4aLDuaxx4ZUoGENJYmA3ws/9hwCg/rN6XxUMbr6zHukzkCDPtZAY5btUXEH/jC63IdAGKX.');
INSERT INTO "user" VALUES(3,'user3','2017-11-28 18:59:19.781644',1,'Another user','$6$rounds=656000$7kb8laXAX3q6szpM$YihcUtpvQV.Agi3WGToDoVIINXCDeBJjM9Z/.dyk66qBc4qIvnrNsYo7F5QV0RFem/Ptijko7891zlE7WKrHm0');
INSERT INTO "user" VALUES(4,'user4','2017-11-28 19:01:02.819949',1,'Another user','$6$rounds=656000$4hmymo1EsqEt6HnP$CcSsH9x839cbDXQ/aDnWPdL7PHn6SKn6kRXaz9Vp/mGYoVzOYdd8XWWqNyfZwEbHB/eXr0sh0kO72bB8srkR51');
INSERT INTO "user" VALUES(5,'user5','2017-11-28 19:02:22.525392',1,'Another user','$6$rounds=656000$mTu9P2Ghceb1cZhJ$NFLileKiZnExfTewSXLsh60clJ.vLYk6uZIscwfJTo0pNdKfouRjXhORExCNfszelEoPq3R7L6T8ruq8uf30C/');
INSERT INTO "user" VALUES(6,'yoshimot','2017-11-30 23:43:57.221171',1,'TBA','$6$rounds=656000$5/IlSQzMLlrJXuZj$htKaSdTBenavITzjipVazbVWSe11ohVNTVtScxXRr2QvmEjAsTvNQzDCb.KezHSbYnnSvJm1e.QhOCSpjA/Md/');
CREATE TABLE container (
	id INTEGER NOT NULL, 
	cid VARCHAR(128), 
	timestamp DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO "container" VALUES(2,'5ca84c2006944677e8b513b7a9ee9b082f82255394306cfa5b00bee072a1d51d','2017-11-28 15:08:36.619385',1);
INSERT INTO "container" VALUES(3,'0c3d2f2094e4c61eeb5292b156a6aef52fba92a648d97067a2bc213a24a9d8b3','2017-11-28 18:57:16.880314',2);
INSERT INTO "container" VALUES(4,'c2b315156563099a4387a15fffebb63ca02a19e32a71cef2c57af3862ca5562f','2017-11-28 18:59:28.307496',3);
INSERT INTO "container" VALUES(5,'4b973a8149996feee1e6fc7a95cb42b541487fe457e5b51bd1edfb91724a0589','2017-11-28 19:01:14.264747',4);
INSERT INTO "container" VALUES(6,'5fd43937699c2b464f9715936677aa214788eb09b001460dcba2bfb16f75e06b','2017-11-28 19:02:31.582769',5);
CREATE UNIQUE INDEX ix_admin_email ON admin (email);
CREATE UNIQUE INDEX ix_admin_nickname ON admin (nickname);
CREATE UNIQUE INDEX ix_user_name ON user (name);
CREATE UNIQUE INDEX ix_container_cid ON container (cid);
COMMIT;
