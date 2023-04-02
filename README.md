# Life_simulation
Для запуска программы нужно:
  1. Перенести все файлы с расширением ".py", "requirements.txt", "sim.db" и папку "resources" в PyCharm;
  2. Установить все зависимости из файла "requirements.txt";
  3. Убедитесь, что версия интерпретатора 3.9
  4. Запустите файл с именем "main.py"
  
  
Краткая инструкция по использованию:
1.	Откройте приложение
2.	Основные элементы в главном окне:
  * Панель инструментов сверху главного окна – представляет набор доступных действий (кнопок)
  *	Строка состояния снизу главного экрана – отображает статистическую информацию для текущего состояния
  *	Область мира справа окна – основная зона отображения визуализации мир
  *	Первый график слева основного окна – график, отображающий общее кол-ва животных в реальном времени
  *	Второй график слева основного окна – график, отображающий кол-во инфицированных животных в реальном времени
  *	Третий график слева основного окна – гистаграмма, отражающая изменение общих характеристик организмов
  *	Таблица доступных штаммов (слева сверху) – позволяет отображать и добавлять штаммы вирусов, а так же заражать ими живые организмы
3.	Измените параметры мира (если необходимо) . Для этого нажмите первую кнопку панели инструментов и введите необходимые значения. Поле изменится, а параметры для животных будут ограничены и сохранятся в базу данных для последующего использования
4.	Нажмите кнопку добавления живых организмов (вторая кнопка). Каждое нажатие добавляет 100 организмов случайным образом
5.	Вы можете задать точечные параметры для животных (третья кнопка)
6.	Вы можете очистить поле при необходимости (четвертая кнопка)
7.	Следующая группа из кнопок (4 шт) на панели инструментов позволяет управлять циклами симуляции: запустить симуляцию, остановить симуляцию, сделать один шаг, а так же изменить скорость симуляции.
8.	Следующая группа из кнопок (3 шт) на панели инструментов позволяет управлять масштабом: растянуть на весь экран, увеличить или уменьшить масштаб.
9.	Следущая кнопка позволяет создать новый штамм вирусов. Нажмите ее и введите параметры нового вируса. Вирус будет добавлен в таблицу доступных штаммов и сохранен в базу данных для последующего использования
10.	Следующая группа из кнопок (4 шт) на панели инструментов позволяет создать пресеты
11.	Из таблицы штаммов вы можете заразить один случайный организм выбранным вирусом, нажав в нужной строке на кнопку с изображением вируса.
12.	Удалить штамм из таблицы можно нажав на кнопку удаления
13.	Запустите симуляцию и наблюдайте за процессом. Во время выполнения симуляции вы можете менять масштаб и добавлять в мир вирусы.



![Предворительный просмотр программы](https://github.com/uplay1007/Life_simulation/blob/main/life_sim_scr.png)
