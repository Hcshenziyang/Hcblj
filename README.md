personal_workstation
├── backend/
│   ├── main.py        # FastAPI 主入口
│   ├── models.py      # 数据模型
│   ├── database.py    # SQLite 连接
│   └── routers/
│       ├── notes.py   # 笔记 API
│       └── ai.py      # AI 调用 API
│
├── frontend/
│   ├── main.py        # PySide6 启动文件
│   ├── ui/
│   │   ├── home.py
│   │   ├── launcher.py
│   │   ├── notes.py
│   │   └── ai.py
│   └── assets/        # 图标/资源
│
└── README.md