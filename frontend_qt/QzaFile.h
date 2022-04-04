//
// Created by qza2468 on 2022/4/3.
//

#ifndef UNTITLED_QZAFILE_H
#define UNTITLED_QZAFILE_H


#include <QMainWindow>
#include <QMap>

namespace Ui {class QzaFile;}

class QNetworkAccessManager;
class QVBoxLayout;
class QNetworkReply;
class QJsonDocument;
class QMessageBox;

class QzaFile: public QMainWindow{
    Q_OBJECT
public:
    QzaFile(QWidget *parent = nullptr);
    ~QzaFile();

    void make_request(const QString &file_path);
    QWidget *createitem(const QString& filename, int type = 0);
    void show_fileinfo_box(const QString& filename);
    void show_files_info();

    void lockScreen();
    void recoverScreen();
public slots:
    void on_path_change_commited();
    void on_requestFinished(QNetworkReply * );
    void on_dir_clicked();
    void on_file_self_clicked();
private:
    Ui::QzaFile *ui;
    QNetworkAccessManager *manager;
    QMap<QString, QVariant> files_info;
};


#endif //UNTITLED_QZAFILE_H
