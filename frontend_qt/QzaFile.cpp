//
// Created by qza2468 on 2022/4/3.
//

#include "QzaFile.h"
#include "ui_QzaFile.h"
#include "globals.h"


#include <QLabel>
#include <QPlainTextEdit>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>

#include <QJsonObject>
#include <QJsonDocument>
#include <QMessageBox>

// thanks to https://stackoverflow.com/questions/4857188/clearing-a-layout-in-qt
// but there is a little bug. i commented it.
void clearLayout(QLayout *layout) {
    if (layout == nullptr)
        return;
    QLayoutItem *item;
    while ((item = layout->takeAt(0))) {
        if (item->layout()) {
            clearLayout(item->layout());
            delete item->layout();
        }
        else if (item->widget()) {
            delete item->widget();
        }
//        delete item;
    }
}


QzaFile::QzaFile(QWidget *parent)
: QMainWindow(parent), ui(new Ui::QzaFile) {
    ui->setupUi(this);

    manager = new QNetworkAccessManager;

    connect(manager, SIGNAL(finished(QNetworkReply *)), this, SLOT(on_requestFinished(QNetworkReply * )));
    connect(ui->ok_button, SIGNAL(clicked(bool)), this, SLOT(on_path_change_commited()));

    path.setPath("/");
    make_request("/");
}

QzaFile::~QzaFile() {
    delete ui;
}

void QzaFile::on_path_change_commited() {
    make_request(ui->path_edit->text());
}

void QzaFile::on_requestFinished(QNetworkReply *reply) {
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

        clearLayout(ui->files_layout->layout());

        files_info = json_doc.toVariant().toMap();
        show_files_info();

        recoverScreen();
        path.setPath(ui->path_edit->text());
        return;
    }

    recoverScreen();
    ui->path_edit->setText(path.toString());
}

void QzaFile::on_dir_clicked() {
    QString filename = sender()->property("myself_file_path").toString();
    Path path_tmp(path);
    path_tmp.appendPath(filename);
    make_request(path_tmp.toString());
}

void QzaFile::on_file_self_clicked() {
    show_fileinfo_box(sender()->property("myself_file_path").toString());
}

void QzaFile::lockScreen() {
    ui->path_edit->setDisabled(true);
    ui->ok_button->setDisabled(true);
}
void QzaFile::recoverScreen() {
    ui->path_edit->setDisabled(false);
    ui->ok_button->setDisabled(false);
}


QWidget *QzaFile::createitem(const QString& filename, int type) {
    auto *widget = new QWidget;
    auto *layout = new QVBoxLayout;
    widget->setLayout(layout);
    auto *pic_button = new QPushButton;
    auto name_label = new QLabel;

    if (filename.length() > 30) {
        name_label->setText(filename.left(30) + "...");
    } else {
        name_label->setText(filename);
    }
    name_label->setAlignment(Qt::AlignCenter);

    QPixmap pic;
    QIcon icon;
    if (type == 0) {
        pic.load(HOME_DIR"assets/file.svg");
    } else if (type == 1) {
        pic.load(HOME_DIR"assets/folder.svg");
    }
    pic_button->setFlat(true);
    icon.addPixmap(pic);
    pic_button->setIcon(icon);
    pic_button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
    pic_button->setIconSize(QSize(200, 200));
    pic_button->setProperty("myself_file_path", filename);
    if (type == 0 or filename == ".") {
        // TODO: show info about the file. connect it to slot
        qDebug() << filename;
        connect(pic_button, SIGNAL(clicked(bool)), this, SLOT(on_file_self_clicked()));
    } else if (type == 1) {
        connect(pic_button, SIGNAL(clicked(bool)), this, SLOT(on_dir_clicked()));
    }

    layout->addWidget(pic_button);
    layout->addWidget(name_label);

    return widget;
}
void QzaFile::show_fileinfo_box(const QString& filename) {
    QDialog dialog(this);
    auto *layout = new QGridLayout;
    dialog.setLayout(layout);

    auto file_info = files_info[filename].toMap();
    QString filetype;
    layout->addWidget(new QLabel("name: "), 0, 0);
    QString filename_processed;
    for (int i = 30; i < filename.length(); i += 30) {
        filename_processed += filename.mid(i, 30) + "\n";
    }
    layout->addWidget(new QLabel(filename_processed), 0, 1);


    if (file_info["st_mode"].toInt() & 0100000)
        filetype = "file";
    else if (file_info["st_mode"].toInt() & 0040000)
        filetype = "dir";
    layout->addWidget(new QLabel("type: "), 1, 0);
    layout->addWidget(new QLabel(filetype), 1, 1);

    QString file_size;
    if (filename == ".") {
        long dir_size = 0;
        long how_many_items = 0;
        for (auto iter = files_info.begin(); iter != files_info.end(); iter++) {
            dir_size += iter.value().toMap()["st_size"].toLongLong();
            how_many_items++;
        }

        QList<QString> size_flags{"B", "KB", "MB", "GB", "TB"};
        int which = 0;
        while (true) {
            if (dir_size / 1024) {
                which++;
                dir_size /= 1024;
            } else {
                break;
            }
        }
        file_size = QString("%1%2 (%3 items)").arg(QString::number(dir_size), size_flags[which], QString::number(how_many_items));
    } else {
        long dir_size = files_info[filename].toMap()["st_size"].toLongLong();
        QList<QString> size_flags{"B", "KB", "MB", "GB", "TB"};
        int which = 0;
        while (true) {
            if (dir_size / 1024) {
                which++;
                dir_size /= 1024;
            } else {
                break;
            }
        }

        file_size = QString("%1%2").arg(QString::number(dir_size), size_flags[which]);
    }

    layout->addWidget(new QLabel("size: "), 2, 0);
    layout->addWidget(new QLabel(file_size), 2, 1);

    time_t atime = file_info["st_atime"].toInt();
    time_t mtime = file_info["st_mtime"].toInt();
    time_t ctime = file_info["st_ctime"].toInt();
    layout->addWidget(new QLabel("atime: "), 3, 0);
    layout->addWidget(new QLabel(QDateTime::fromSecsSinceEpoch(atime).toString()), 3, 1);
    layout->addWidget(new QLabel("atime: "), 4, 0);
    layout->addWidget(new QLabel(QDateTime::fromSecsSinceEpoch(atime).toString()), 4, 1);
    layout->addWidget(new QLabel("atime: "), 5, 0);
    layout->addWidget(new QLabel(QDateTime::fromSecsSinceEpoch(atime).toString()), 5, 1);

    dialog.exec();
}
void QzaFile::make_request(const QString &file_path) {
    ui->path_edit->setText(file_path);

    QNetworkRequest request;
    request.setUrl(QUrl(URL_BASE"files/ls"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setRawHeader("token", user_token.toUtf8());

    QJsonObject json_send;
    json_send["filepath"] = file_path;
    manager->post(request, QJsonDocument(json_send).toJson());

    lockScreen();
}
void QzaFile::show_files_info() {
    QList<QString> files_list;
    QList<QString> dirs_list;
    for(auto it = files_info.begin();it != files_info.end();++it) {
        if (it.key()[0] == '.') {
            continue;
        }
        auto info = it.value().toMap();
        if (info["st_mode"].toInt() & 0040000)
            dirs_list.append(it.key());
        else if (info["st_mode"].toInt() & 0100000)
            files_list.append(it.key());
    }

    dirs_list.sort(Qt::CaseInsensitive);
    files_list.sort(Qt::CaseInsensitive);
    for (auto & it : dirs_list) {
        ui->files_layout->insertWidget(-1, createitem(it, 1));
    }
    for (auto & it : files_list) {
        ui->files_layout->insertWidget(-1, createitem(it, 0));
    }

    auto spacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
    ui->files_layout->insertItem(-1, spacer);

    ui->files_layout->insertWidget(0, createitem(".", 1));
    ui->files_layout->insertWidget(0, createitem("..", 1));
}

