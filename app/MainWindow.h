#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QVBoxLayout>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QLineEdit>
#include <QLabel>
#include <QDialog>
#include <QProcess>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void startSetup();
    void handleReply();
    void handleAccept();
    void handleDecline();

private:
    QLineEdit *lineEdit;
    QPushButton *setupButton;
    QNetworkAccessManager *networkManager;
    QString current_user_name;
    QString cacheFilePath;
    QString dataFilePath;
    QDialog *popup;


    void openPopup();
};

#endif // MAINWINDOW_H
