//
// Created by qza2468 on 2022/4/4.
//

#ifndef UNTITLED_PATH_H
#define UNTITLED_PATH_H

#include <QList>
class QString;

class Path {
public:
    Path() = default;
    explicit Path(const QString &s);
    void setPath(const QString &s);
    QString toString();
    void appendPath(const QString &s);
    void goParent();

private:
    QList<QString> components;
};


#endif //UNTITLED_PATH_H
