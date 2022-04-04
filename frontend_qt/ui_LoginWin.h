/********************************************************************************
** Form generated from reading UI file 'LoginWin.ui'
**
** Created by: Qt User Interface Compiler version 6.2.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LOGINWIN_H
#define UI_LOGINWIN_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_LoginWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QSpacerItem *verticalSpacer;
    QLabel *title;
    QSpacerItem *verticalSpacer_5;
    QHBoxLayout *horizontalLayout;
    QLabel *username_label;
    QLineEdit *username_edit;
    QSpacerItem *verticalSpacer_2;
    QHBoxLayout *horizontalLayout_2;
    QLabel *password_label;
    QLineEdit *password_edit;
    QSpacerItem *verticalSpacer_4;
    QHBoxLayout *horizontalLayout_3;
    QSpacerItem *horizontalSpacer;
    QPushButton *login_button;
    QSpacerItem *horizontalSpacer_2;
    QLabel *error_message;
    QSpacerItem *verticalSpacer_3;

    void setupUi(QMainWindow *LoginWindow)
    {
        if (LoginWindow->objectName().isEmpty())
            LoginWindow->setObjectName(QString::fromUtf8("LoginWindow"));
        LoginWindow->resize(575, 717);
        centralwidget = new QWidget(LoginWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setSizeConstraint(QLayout::SetDefaultConstraint);
        verticalLayout->setContentsMargins(32, 9, 32, -1);
        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);

        title = new QLabel(centralwidget);
        title->setObjectName(QString::fromUtf8("title"));
        QFont font;
        font.setPointSize(36);
        title->setFont(font);
        title->setLineWidth(1);
        title->setAlignment(Qt::AlignCenter);
        title->setMargin(0);
        title->setIndent(-1);

        verticalLayout->addWidget(title);

        verticalSpacer_5 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer_5);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setSizeConstraint(QLayout::SetDefaultConstraint);
        username_label = new QLabel(centralwidget);
        username_label->setObjectName(QString::fromUtf8("username_label"));
        username_label->setEnabled(true);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(username_label->sizePolicy().hasHeightForWidth());
        username_label->setSizePolicy(sizePolicy);
        username_label->setMinimumSize(QSize(112, 0));

        horizontalLayout->addWidget(username_label);

        username_edit = new QLineEdit(centralwidget);
        username_edit->setObjectName(QString::fromUtf8("username_edit"));
        QSizePolicy sizePolicy1(QSizePolicy::Minimum, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(200);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(username_edit->sizePolicy().hasHeightForWidth());
        username_edit->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(username_edit);

        horizontalLayout->setStretch(1, 1);

        verticalLayout->addLayout(horizontalLayout);

        verticalSpacer_2 = new QSpacerItem(20, 20, QSizePolicy::Minimum, QSizePolicy::Fixed);

        verticalLayout->addItem(verticalSpacer_2);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalLayout_2->setSizeConstraint(QLayout::SetDefaultConstraint);
        password_label = new QLabel(centralwidget);
        password_label->setObjectName(QString::fromUtf8("password_label"));
        sizePolicy.setHeightForWidth(password_label->sizePolicy().hasHeightForWidth());
        password_label->setSizePolicy(sizePolicy);
        password_label->setMinimumSize(QSize(112, 0));

        horizontalLayout_2->addWidget(password_label);

        password_edit = new QLineEdit(centralwidget);
        password_edit->setObjectName(QString::fromUtf8("password_edit"));
        QSizePolicy sizePolicy2(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(password_edit->sizePolicy().hasHeightForWidth());
        password_edit->setSizePolicy(sizePolicy2);

        horizontalLayout_2->addWidget(password_edit);


        verticalLayout->addLayout(horizontalLayout_2);

        verticalSpacer_4 = new QSpacerItem(20, 32, QSizePolicy::Minimum, QSizePolicy::Fixed);

        verticalLayout->addItem(verticalSpacer_4);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setSpacing(0);
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        horizontalLayout_3->setContentsMargins(0, 0, -1, -1);
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer);

        login_button = new QPushButton(centralwidget);
        login_button->setObjectName(QString::fromUtf8("login_button"));
        login_button->setAutoFillBackground(false);
        login_button->setFlat(false);

        horizontalLayout_3->addWidget(login_button);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_2);


        verticalLayout->addLayout(horizontalLayout_3);

        error_message = new QLabel(centralwidget);
        error_message->setObjectName(QString::fromUtf8("error_message"));
        error_message->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(error_message);

        verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer_3);

        verticalLayout->setStretch(0, 2);
        verticalLayout->setStretch(2, 3);
        verticalLayout->setStretch(9, 5);
        LoginWindow->setCentralWidget(centralwidget);

        retranslateUi(LoginWindow);

        QMetaObject::connectSlotsByName(LoginWindow);
    } // setupUi

    void retranslateUi(QMainWindow *LoginWindow)
    {
        LoginWindow->setWindowTitle(QCoreApplication::translate("LoginWindow", "MainWindow", nullptr));
        title->setText(QCoreApplication::translate("LoginWindow", "QZAFile", nullptr));
        username_label->setText(QCoreApplication::translate("LoginWindow", "username: ", nullptr));
        password_label->setText(QCoreApplication::translate("LoginWindow", "password: ", nullptr));
        login_button->setText(QCoreApplication::translate("LoginWindow", "login", nullptr));
        error_message->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class LoginWindow: public Ui_LoginWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LOGINWIN_H
