//
// Created by qza2468 on 2022/4/4.
//

#include "Path.h"

Path::Path(const QString &s) {
    setPath(s);
}

void Path::setPath(const QString &s) {
    components.clear();
    auto parts = s.split('/', Qt::SkipEmptyParts);
    for (const auto& part: parts) {
        appendPath(part);
    }
}

QString Path::toString() {
    QString res = "/";
    for (auto & component : components) {
        res += component + '/';
    }

    return res;
}

void Path::appendPath(const QString &s) {
    if (s == ".") {
        return;
    }

     if (s == "..") {
        goParent();
    } else {
        components.push_back(s);
    }
}

void Path::goParent() {
    if (not components.empty()) {
        components.pop_back();
    }
}