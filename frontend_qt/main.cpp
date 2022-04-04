#include <QApplication>
#include <QPushButton>

#include "LoginWin.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    LoginWin w;
    w.show();
    return a.exec();
}
