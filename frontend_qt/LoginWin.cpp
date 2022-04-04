//
// Created by qza2468 on 2022/4/3.
//

#include "LoginWin.h"
#include "ui_LoginWin.h"
#include "globals.h"
#include "QzaFile.h"


#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QtNetwork/QNetworkRequest>
#include <QJsonObject>
#include <QJsonDocument>
#include <QMessageBox>

LoginWin::LoginWin(QWidget *parent)
: QMainWindow(parent), ui(new Ui::LoginWindow){
    ui->setupUi(this);
    manager = new QNetworkAccessManager(this);
    connect(manager, SIGNAL(finished(QNetworkReply *)), this, SLOT(on_requestFinished(QNetworkReply * )));
    connect(ui->login_button, SIGNAL(pressed()), this, SLOT(on_loginCommitted()));
}

void LoginWin::on_requestFinished(QNetworkReply *reply) {
    while (true) {
        if (reply->error() != QNetworkReply::NoError) {
            QMessageBox::information(this, "error", reply->errorString());
            qDebug() << reply->errorString();
            break;
        }

        QJsonParseError error;

        QJsonDocument json_doc = QJsonDocument::fromJson(reply->readAll(), &error);

        if (error.error != QJsonParseError::NoError and json_doc.isNull()) {
            QMessageBox::information(this, "error", "parse res json error");
            qDebug() << error.errorString();
            qDebug() << "what shit";
            break;
        }

        auto json_res = json_doc.toVariant().toMap();
        if (not json_res["ok"].toBool()) {
            ui->error_message->setText(json_res["message"].toString());
            qDebug() << json_res["message"].toString();
            break;
        }

        user_token = json_res["token"].toString();
        qDebug() << user_token;

        // transfer to another window.
        this->hide();
        auto *qzaFile = new QzaFile(this);
        qzaFile->show();
        break;
    }

    ui->login_button->setDisabled(false);
    ui->username_edit->setDisabled(false);
    ui->password_edit->setDisabled(false);
}

void LoginWin::on_loginCommitted() {
    ui->login_button->setDisabled(true);
    ui->username_edit->setDisabled(true);
    ui->password_edit->setDisabled(true);
    ui->error_message->setText("");

    QNetworkRequest request;
    request.setUrl(QUrl(URL_BASE"login"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject push_data;
    push_data["name"] = ui->username_edit->text();
    push_data["password"] = ui->password_edit->text();
    QJsonDocument doc(push_data);

    qDebug() << doc.toJson();
    manager->post(request, doc.toJson());
}

LoginWin::~LoginWin() {
    delete ui;
}