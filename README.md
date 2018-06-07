# ТРЕКЕР ДЕЛ Adastra
Adastra предназначен для создания проектов, списков задач и задач, а также управления ими.
Имеются возможности создания нескольких пользователей и добавления их к проектам.
Также реализована возможность создания плановых задач.

## Клонирование ##
```bash
$ git clone https://Eugene_Kachanovski@bitbucket.org/Eugene_Kachanovski/isp_business_tracker.git
```

## Установка ##
### Установка библиотеки: ###
```bash
$ python3.6 -m pip install [путь к директории]/adastra_library/
```

### Установка приложения (консольный интерфейс): ###
```bash
$ python3.6 -m pip install [путь к директории]
```

## Пример использования ##
### Создание пользователя ###
```bash
$ adastra user add Mary
```

### Смена пользователя ###
```bash
$ adastra chuser 9a91dcfe-a0d1-436b-9e99-fb76d6bada62
```

### Создание проекта ###
```bash
$ adastra project add "Making party"
```

### Переход на проект ###
```bash
$ adastra checkout 9a4d0be4-6ba0-4d77-b1c7-4357dacc8780
```

### Добавление списка ###
```bash
$ adastra list add "Buy balloons"
```

### Добавление задач ###
```bash
$ adastra task add b6fa454f-670e-48af-8349-ec0de1be583e "Buy red balloons"
$ adastra task add b6fa454f-670e-48af-8349-ec0de1be583e "Buy blue balloons"
```

### Добавление пользователя к проекту ###
```bash
$ adastra user add John
$ adastra upr add 463c9e0f-e058-4fe2-9fcb-9fb67981a299
```

*Для более подробной документации используйте флаг -h*
