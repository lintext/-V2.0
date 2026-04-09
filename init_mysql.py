#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL 数据库初始化脚本
创建数据库和所有必要的表
"""

import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'xiaoai',
    'charset': 'utf8mb4'
}

CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(100) DEFAULT 'default',
        role ENUM('user', 'assistant', 'system') NOT NULL,
        content TEXT NOT NULL,
        emotion VARCHAR(50) DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_chat_session_id (session_id),
        INDEX idx_chat_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS system_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level ENUM('info', 'warning', 'error', 'debug') NOT NULL,
        source VARCHAR(100) DEFAULT NULL,
        message TEXT NOT NULL,
        details TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_logs_level (level),
        INDEX idx_logs_source (source),
        INDEX idx_logs_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS user_interactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(100) DEFAULT 'default',
        interaction_type VARCHAR(50) NOT NULL,
        details TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_interactions_session_id (session_id),
        INDEX idx_interactions_type (interaction_type)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS app_config (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(100) NOT NULL,
        `key` VARCHAR(100) NOT NULL,
        value TEXT NOT NULL,
        description TEXT DEFAULT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uk_category_key (category, `key`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS plugins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        display_name VARCHAR(100) NOT NULL,
        description TEXT DEFAULT NULL,
        version VARCHAR(20) DEFAULT '1.0.0',
        enabled BOOLEAN DEFAULT TRUE,
        config TEXT DEFAULT NULL,
        installed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS tools (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        display_name VARCHAR(100) NOT NULL,
        description TEXT DEFAULT NULL,
        type VARCHAR(50) DEFAULT 'builtin',
        enabled BOOLEAN DEFAULT TRUE,
        config TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(100) NOT NULL UNIQUE,
        name VARCHAR(100) DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        message_count INT DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
]

def init_database():
    """初始化数据库和表"""
    print('正在连接 MySQL...')
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        charset=DB_CONFIG['charset']
    )
    print('连接成功!')
    
    cursor = conn.cursor()
    
    print('正在创建数据库 xiaoai...')
    cursor.execute('CREATE DATABASE IF NOT EXISTS xiaoai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    print('数据库 xiaoai 创建成功!')
    
    cursor.execute('USE xiaoai')
    conn.select_db('xiaoai')
    
    print('正在创建数据表...')
    for i, sql in enumerate(CREATE_TABLES_SQL):
        try:
            cursor.execute(sql)
            print(f'  表 {i+1} 创建成功')
        except Exception as e:
            print(f'  表 {i+1} 创建失败: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()
    print('\n数据库初始化完成!')
    print('数据库: xiaoai')
    print('表: chat_messages, system_logs, user_interactions, app_config, plugins, tools, sessions')

if __name__ == '__main__':
    init_database()
