/********************************************************************************
** Form generated from reading UI file 'QzaFile.ui'
**
** Created by: Qt User Interface Compiler version 6.2.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_QZAFILE_H
#define UI_QZAFILE_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_QzaFile
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout_2;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QLabel *title;
    QPushButton *info_button;
    QHBoxLayout *horizontalLayout_2;
    QLineEdit *path_edit;
    QPushButton *ok_button;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidget;
    QVBoxLayout *files_layout;
    QSpacerItem *verticalSpacer;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout_2 = new QVBoxLayout(centralwidget);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setSizeConstraint(QLayout::SetMinAndMaxSize);
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        title = new QLabel(centralwidget);
        title->setObjectName(QString::fromUtf8("title"));

        horizontalLayout->addWidget(title);

        info_button = new QPushButton(centralwidget);
        info_button->setObjectName(QString::fromUtf8("info_button"));
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(info_button->sizePolicy().hasHeightForWidth());
        info_button->setSizePolicy(sizePolicy);

        horizontalLayout->addWidget(info_button);


        verticalLayout->addLayout(horizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        path_edit = new QLineEdit(centralwidget);
        path_edit->setObjectName(QString::fromUtf8("path_edit"));

        horizontalLayout_2->addWidget(path_edit);

        ok_button = new QPushButton(centralwidget);
        ok_button->setObjectName(QString::fromUtf8("ok_button"));

        horizontalLayout_2->addWidget(ok_button);


        verticalLayout->addLayout(horizontalLayout_2);

        scrollArea = new QScrollArea(centralwidget);
        scrollArea->setObjectName(QString::fromUtf8("scrollArea"));
        scrollArea->setWidgetResizable(true);
        scrollAreaWidget = new QWidget();
        scrollAreaWidget->setObjectName(QString::fromUtf8("scrollAreaWidget"));
        scrollAreaWidget->setGeometry(QRect(0, 0, 778, 500));
        files_layout = new QVBoxLayout(scrollAreaWidget);
        files_layout->setObjectName(QString::fromUtf8("files_layout"));
        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        files_layout->addItem(verticalSpacer);

        scrollArea->setWidget(scrollAreaWidget);

        verticalLayout->addWidget(scrollArea);


        verticalLayout_2->addLayout(verticalLayout);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("QzaFile", "MainWindow", nullptr));
        title->setText(QCoreApplication::translate("QzaFile", "TextLabel", nullptr));
        info_button->setText(QCoreApplication::translate("QzaFile", "i", nullptr));
        ok_button->setText(QCoreApplication::translate("QzaFile", "ok", nullptr));
    } // retranslateUi

};

namespace Ui {
    class QzaFile: public Ui_QzaFile {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_QZAFILE_H
