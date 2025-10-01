# Hospital Management API Documentation

## Доступні Endpoints

### Пацієнти (Patients)

- `GET /patients` - Отримати список всіх пацієнтів
- `GET /patients/<id>` - Отримати пацієнта за ID
- `POST /patients` - Створити нового пацієнта
- `PUT /patients/<id>` - Оновити пацієнта
- `DELETE /patients/<id>` - Видалити пацієнта
- `POST /patients/dummy` - Додати тестові дані

### Лікарі (Doctors)

- `GET /doctors` - Отримати список всіх лікарів
- `GET /doctors/<id>` - Отримати лікаря за ID
- `POST /doctors` - Створити нового лікаря
- `PUT /doctors/<id>` - Оновити лікаря
- `DELETE /doctors/<id>` - Видалити лікаря
- `GET /doctors/hospitals/<hospital_id>` - Отримати лікарів за лікарнею

### Лікарні (Hospitals)

- `GET /hospitals` - Отримати список всіх лікарень
- `GET /hospitals/<id>` - Отримати лікарню за ID
- `POST /hospitals` - Створити нову лікарню
- `PUT /hospitals/<id>` - Оновити лікарню
- `DELETE /hospitals/<id>` - Видалити лікарню
- `POST /create_databases` - Створити бази даних

### Медикаменти (Medications)

- `GET /medications` - Отримати список всіх медикаментів
- `GET /medications/<id>` - Отримати медикамент за ID
- `POST /medications` - Створити новий медикамент
- `PUT /medications/<id>` - Оновити медикамент
- `DELETE /medications/<id>` - Видалити медикамент

### Призначення медикаментів (Patient Medications)

- `GET /patient_medications` - Отримати список всіх призначень
- `GET /patient_medications/<id>` - Отримати призначення за ID
- `POST /patient_medications` - Створити нове призначення
- `PUT /patient_medications/<id>` - Оновити призначення
- `DELETE /patient_medications/<id>` - Видалити призначення
- `GET /patients/<patient_id>/medications` - Отримати медикаменти пацієнта
- `GET /medications/<medication_id>/patients` - Отримати пацієнтів для медикаменту

### Відділення (Departments)

- `GET /departments` - Отримати список всіх відділень
- `GET /departments/<id>` - Отримати відділення за ID
- `POST /departments` - Створити нове відділення
- `PUT /departments/<id>` - Оновити відділення
- `DELETE /departments/<id>` - Видалити відділення

### Агрегатні функції (Aggregates)

- `GET /aggregates` - Отримати агрегатні дані

### Історія логів (History Logs)

- `GET /history_logs` - Отримати історію логів

### Трекер пацієнтів (Patient Tracker)

- `GET /patient_trackers` - Отримати дані трекера пацієнтів

## Swagger UI

Інтерактивна документація доступна за адресою: `/api/v1/swagger/`

## Приклад використання

```bash
# Отримати всіх пацієнтів
curl http://localhost:5000/patients

# Створити нового пацієнта
curl -X POST http://localhost:5000/patients \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Іван", "last_name": "Петренко", "date_of_birthday": "1990-01-01", "gender": "Male", "address": "Київ", "phone": "1234567890"}'
```
