//
// Created by qza2468 on 2022/4/3.
//

#ifndef UNTITLED_LOGINWIN_H
#define UNTITLED_LOGINWIN_H

#include <QMainWindow>

class QNetworkReply;
class QNetworkAccessManager;


namespace Ui {class LoginWindow;};

class LoginWin: public QMainWindow {
    Q_OBJECT
public:
    LoginWin(QWidget *parent = nullptr);
    ~LoginWin();

private slots:
    void on_requestFinished(QNetworkReply *reply);
    void on_loginCommitted();
private:
    Ui::LoginWindow *ui;
    QNetworkAccessManager *manager;
};


#endif //UNTITLED_LOGINWIN_H
