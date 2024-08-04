#include "MainWindow.h"
#include <QNetworkRequest>
#include <QJsonDocument>
#include <QJsonObject>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      lineEdit(new QLineEdit(this)),
      setupButton(new QPushButton("Add user", this)),
      networkManager(new QNetworkAccessManager(this)),
      cacheFilePath("/home/luky/playground/face_recognition_unlock/app/cache"),
      dataFilePath("/home/luky/playground/face_recognition_unlock/app/data")

{    
    // Layout
    QVBoxLayout *layout = new QVBoxLayout;

    layout->addWidget(lineEdit);
    layout->addWidget(setupButton);

    QWidget *centralWidget = new QWidget(this);
    centralWidget->setLayout(layout);
    setCentralWidget(centralWidget);


    // Connect the button to the slot
    connect(setupButton, &QPushButton::clicked, this, &MainWindow::startSetup);
}

MainWindow::~MainWindow()
{

}

void MainWindow::startSetup()
{
    QString text = lineEdit->text();
    // Create the request
    QNetworkRequest request(QUrl("http://localhost:8080/start-setup")); // Adjust the URL as needed

    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    // Create JSON payload
    QJsonObject json;
    json["action"] = "start_setup";
    json["user_name"] = text;
    current_user_name = text;
    QJsonDocument doc(json);

    // Send POST request
    QNetworkReply *reply = networkManager->post(request, doc.toJson());

    // Connect the reply to the handleReply slot
    connect(reply, &QNetworkReply::finished, this, &MainWindow::handleReply);
}

void MainWindow::handleReply()
{
    QNetworkReply *reply = qobject_cast<QNetworkReply *>(sender());
    if (reply->error() == QNetworkReply::NoError) {
        qDebug() << "Setup started successfully";
        openPopup();
    } else {
        qDebug() << "Error starting setup:" << reply->errorString();

        // Handle error here
        // For example, show an error message
    }
    reply->deleteLater();
}


void MainWindow::openPopup(){
    popup = new QDialog(this);
    popup->setWindowTitle("Add user");
    QVBoxLayout *popupLayout = new QVBoxLayout(popup);
     // Create and add a label to the layout
    QLabel *label = new QLabel(QString("Are you sure you want to add new user named %1?").arg(current_user_name), popup);
    popupLayout->addWidget(label);

    // Create and add "Accept" and "Decline" buttons to the layout
    QPushButton *acceptButton = new QPushButton("Yes", popup);
    QPushButton *declineButton = new QPushButton("No", popup);
    QHBoxLayout *buttonLayout = new QHBoxLayout;
    buttonLayout->addWidget(acceptButton);
    buttonLayout->addWidget(declineButton);
    popupLayout->addLayout(buttonLayout);

    // Connect the buttons to their respective slots
    connect(acceptButton, &QPushButton::clicked, this, &MainWindow::handleAccept);
    connect(declineButton, &QPushButton::clicked, this, &MainWindow::handleDecline);

    // Show the dialog
    popup->exec();
}


// Copy cache into data folder
void MainWindow::handleAccept()
{
    QString command = QString("cp -r %1/* %2/").arg(cacheFilePath).arg(dataFilePath);

    if (QProcess::execute("bash", QStringList() << "-c" << command) == 0) {
        qDebug() << "Copied files successfully";
    } else {
        qDebug() << "Failed to copy files";
    }

    popup->accept();  // Close the popup dialog
}

// Remove cache 
void MainWindow::handleDecline()
{
    QString command = QString("rm -rf %1/*").arg(cacheFilePath);

    if (QProcess::execute("bash", QStringList() << "-c" << command) == 0) {
        qDebug() << "Removed files successfully";
    } else {
        qDebug() << "Failed to remove files";
    }

    popup->reject();  // Close the popup dialog
}
