//#include <Winsock2.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <stdio.h>
#include <fstream>
#include <string>
#include <iostream>
#include <cstring>
#include <stdlib.h>
//#define FALSE 0
//#define SOCKET_ERROR (-1)
#include <unistd.h>
//#pragma comment(lib,"wsock32.lib")
using namespace std;
typedef unsigned char BYTE;
typedef unsigned long DWORD;
typedef int SOCKET;

typedef unsigned short    WORD;


//#import "C:\Program Files\BCL Technologies\easyConverter SDK 4\HTML\beconvh.dll"

#define PERSIZE 102400
#define PDFNAME "PDF.zip"

string serverip = "159.226.208.186";


int sendFile(ifstream *readFile, SOCKET cli_s);
int recvfile(SOCKET ser_c, string filename, string workpath);

int main(int argc, char **argv)
{
	if(argc < 2)
	{
		cout << "no argv:input workpath"<<endl;
		return -2;
	}
	string PATH = string(argv[1])+"/";
	string FILE = PATH + PDFNAME;
	cout << PATH << argv[1]<< endl;

	ifstream readFile;
	readFile.open(FILE.c_str(), ios::binary); //二进制打开
	if(!readFile)
	{
		cout << "open false\n";
		return -1;
	}

	
	

	printf("send %s, filename : %s\n", PATH.c_str(), FILE.c_str());
    //固定格式
    /*WORD wVersionRequested;
    WSADATA wsaData;
    int err;
    
    wVersionRequested = MAKEWORD( 1, 1 );
    
    err = WSAStartup( wVersionRequested, &wsaData );
    if ( err != 0 ) {
        return -1;
    }
    

    if ( LOBYTE( wsaData.wVersion ) != 1 ||
        HIBYTE( wsaData.wVersion ) != 1 ) {
        WSACleanup( );
        return -1; 
    }*/

    //建立通讯socket
    SOCKET sockClient=socket(AF_INET,SOCK_STREAM,0);

    //SOCKADDR_IN addrSrv;
	sockaddr_in addrSrv;
	//addrSrv.sin_addr.S_un.S_addr=inet_addr(serverip.c_str());//设定需要链接的服务器的IP地址
	addrSrv.sin_addr.s_addr=inet_addr(serverip.c_str());
    addrSrv.sin_family=AF_INET;
    addrSrv.sin_port=htons(10428);//设定需要连接的服务器的端口地址
    if(connect(sockClient,(sockaddr*)&addrSrv,sizeof(sockaddr)) < 0 )//与服务器进行连接
	{
		printf("can't connect server\n");
		exit(0);
	}
	printf("已连接Server\n");
	//接受来自SERER的信息
	char recvBuf[1024] = {0};
	char sendBuf[1024] = {0};
	int recvLen;

    //发送消息给Server
	printf("input message:");

	while(1)
	{

		send(sockClient,"file",strlen("file")+1,0);
		if((recvLen = recv(sockClient,recvBuf,1024,0)) > 0)
		{
			recvBuf[recvLen] = '\0';
			printf("recv£º%s\n",recvBuf);
			if(!strcmp(recvBuf,"recvnow"))
			{

				printf("start sendfile:%s\n", FILE.c_str());
				sendFile(&readFile, sockClient);
				sleep(100);
				recvfile(sockClient, "htm.zip", PATH);
				return 0;
			}
			printf("input message:");
		}
	}

    close(sockClient);
    //WSACleanup();
	return 0;
}

int sendFile(ifstream *readFile, SOCKET cli_s)
{
	char sendBuf[PERSIZE] = {0};
    int readBytes;

	
	readFile->seekg(0, ios::end);			//定位文件尾部
	int end = (int) readFile->tellg();		//文件结束位置
	readFile->seekg(0, ios::beg);			//定位文件头部
	int start = (int) readFile->tellg();		//文件起始位置
	int FileLen = end - start;			//获取文件长度


	printf("file lengs :%d Bytes,size: %d\n",FileLen, sizeof(FileLen));
	send(cli_s, (char *)&FileLen, 4, 0); //·¢ËÍÎÄŒþ³€¶È
    while (1)
	{
		if(readFile->eof())
		{
			break;
		}
		readBytes = (int)readFile->read(sendBuf, sizeof(sendBuf)).gcount();
		printf("read %d bytes\n", readBytes);

		if (readBytes>0) //逐个发送,直到读不出数据
		{
			send(cli_s, sendBuf, readBytes, 0);
			sleep(10);
		}
	}
    readFile->close();
	cout << "send file over"<<endl;
	return 0;
}

int recvfile(SOCKET ser_c, string filename, string workpath)	//接受文件
{
	printf("start recv %s\n", filename.c_str());
	char recvBuf[PERSIZE] = {0};
	int recvLen;
	int FileLen;
	string file = workpath + filename;
	int view = 0;

	if((recvLen = recv(ser_c,(char *)&FileLen,4,0)) > 0)
	{
		printf("fileLen: %d\n", FileLen);
		ofstream writeFile(file.c_str(),ios::binary);
		//memset
		while(FileLen > 0)
		{
			if((recvLen = recv(ser_c, recvBuf, PERSIZE, 0)) < 0)
			{
				return 1;
			}
			writeFile.write(recvBuf, recvLen);
			cout << "recv:" << recvLen << "Bytes" << endl;
			view += recvLen;
			FileLen -= recvLen;
		}
		writeFile.close();
		cout << "recv total " << view << " Bytes" << endl;
	}
	return 0;
}
