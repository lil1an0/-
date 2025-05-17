- 账号：superadmin
- 密码：admin123456


环境
	Python >= 3.11.0 (最低3.9+版本)     
	nodejs >= 16.0
	Mysql >= 8.0 (可选，默认数据库sqlite3，支持5.7+，推荐8.0版本)

前端
	1、cd web
	2、npm install yarn   如果电脑有yarn就不用安装了
	3、yarn install --registry=https://registry.npmmirror.com
	4、yarn build
	5、npm install   如果电脑有yarn 前面 2.3.4 步骤可以省略，直接运行5
	6、npm run dev
	7、访问http://localhost:8080 此时前端项目已经启动


后端
	1. cd backend
	2. 在 env.py 中配置数据库信息
	3. 安装依赖环境 pip3 install -r requirements.txt
	4. 执行迁移命令：
		python3 manage.py makemigrations
		python3 manage.py migrate
	5. 初始化数据
		python3 manage.py init
	6. 初始化省市县数据:
		python3 manage.py init_area
	7. 启动项目
		python3 manage.py runserver 0.0.0.0:8000    此时后端项目已经启动


10 11 月份为算法预测价格走势 预测价格走势比较平缓

品牌售卖分析

访问项目
	- 访问地址：[http://localhost:8080](http://localhost:8080) (默认为此地址，如有修改请按照配置文件)
	- 账号：`superadmin` 密码：`admin123456`
