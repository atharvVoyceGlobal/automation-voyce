import matplotlib.pyplot as plt

# Данные о пользователях и времени отклика
data = [
    {'Email': 'nikita.qahud0', 'Response Time': 14.811160326004028},
    {'Email': 'nikita.qahud1', 'Response Time': 11.739346504211426},
    {'Email': 'nikita.qahud2', 'Response Time': 15.443873643875122},
    {'Email': 'nikita.qahud3', 'Response Time': 15.440504550933838},
    {'Email': 'nikita.qahud4', 'Response Time': 12.742431163787842},
    {'Email': 'nikita.qahud5', 'Response Time': 11.768094539642334},
    {'Email': 'nikita.qahud6', 'Response Time': 13.4115629196167},
    {'Email': 'nikita.qahud7', 'Response Time': 14.405034303665161},
    {'Email': 'nikita.qahud8', 'Response Time': 18.02180051803589},
    {'Email': 'nikita.qahud9', 'Response Time': 15.69552993774414},
    {'Email': 'nikita.qahud11', 'Response Time': 11.01301908493042},
    {'Email': 'nikita.qahud12', 'Response Time': 11.116509914398193},
    {'Email': 'nikita.qahud13', 'Response Time': 11.47667932510376},
    {'Email': 'nikita.qahud14', 'Response Time': 12.037940979003906},
    {'Email': 'nikita.qahud15', 'Response Time': 11.57000994682312},
    {'Email': 'nikita.qahud16', 'Response Time': 11.437597036361694},
    {'Email': 'nikita.qahud17', 'Response Time': 11.454114198684692},
    {'Email': 'nikita.qahud18', 'Response Time': 11.464935064315796},
    {'Email': 'nikita.qahud19', 'Response Time': 11.108819961547852},
    {'Email': 'nikita.qahud20', 'Response Time': 11.258167028427124},
    {'Email': 'nikita.qahud21', 'Response Time': 14.301114797592163},  # Изменено время
    {'Email': 'nikita.qahud28', 'Response Time': 11.000874996185303},
    {'Email': 'nikita.qahud29', 'Response Time': 10.998773097991943},
    {'Email': 'nikita.qahud30', 'Response Time': 11.48081088066101},
    {'Email': 'nikita.qahud31', 'Response Time': 11.266668796539307},
    {'Email': 'nikita.qahud32', 'Response Time': 11.342916011810303},
    {'Email': 'nikita.qahud33', 'Response Time': 11.704816818237305},
    {'Email': 'nikita.qahud34', 'Response Time': 11.41864800453186},
    {'Email': 'nikita.qahud35', 'Response Time': 11.27738904953003},
    {'Email': 'nikita.qahud36', 'Response Time': 11.63133716583252},
    {'Email': 'nikita.qahud38', 'Response Time': 11.228969097137451},
    {'Email': 'nikita.qahud39', 'Response Time': 11.907958984375},
    {'Email': 'nikita.qahud40', 'Response Time': 13.034974098205566},
    {'Email': 'nikita.qahud37', 'Response Time': 13.099606990814209},
    {'Email': 'nikita.qahud41', 'Response Time': 14.926811933517456},  # Изменено время
    {'Email': 'nikita.qahud42', 'Response Time': 13.89576768875122},
    {'Email': 'nikita.qahud43', 'Response Time': 11.319033145904541},
    {'Email': 'nikita.qahud44', 'Response Time': 11.907383918762207},
    {'Email': 'nikita.qahud45', 'Response Time': 13.409463882446289},
    {'Email': 'nikita.qahud46', 'Response Time': 11.458726167678833},
    {'Email': 'nikita.qahud48', 'Response Time': 11.428020000457764},
    {'Email': 'nikita.qahud47', 'Response Time': 11.406532049179077},
    {'Email': 'nikita.qahud49', 'Response Time': 11.687000751495361},
    {'Email': 'nikita.qahud50', 'Response Time': 11.415801048278809},
    {'Email': 'nikita.qahud51', 'Response Time': 12.137009859085083},
    {'Email': 'nikita.qahud52', 'Response Time': 11.334629774093628},
    {'Email': 'nikita.qahud53', 'Response Time': 11.010015964508057},
    {'Email': 'nikita.qahud54', 'Response Time': 11.3160080909729},
    {'Email': 'nikita.qahud55', 'Response Time': 12.4552321434021},
    {'Email': 'nikita.qahud56', 'Response Time': 10.956400871276855},
    {'Email': 'nikita.qahud57', 'Response Time': 11.469576120376587},
    {'Email': 'nikita.qahud58', 'Response Time': 11.673131942749023},
    {'Email': 'nikita.qahud60', 'Response Time': 11.323153257369995},
    {'Email': 'nikita.qahud59', 'Response Time': 11.282917261123657},
    {'Email': 'nikita.qahud61', 'Response Time': 12.992043018341064},
    {'Email': 'nikita.qahud62', 'Response Time': 14.436739206314087},  # Изменено время
    {'Email': 'nikita.qahud63', 'Response Time': 13.355425119400024},
    {'Email': 'nikita.qahud65', 'Response Time': 11.596979141235352},
    {'Email': 'nikita.qahud64', 'Response Time': 11.17844009399414},
    {'Email': 'nikita.qahud66', 'Response Time': 18.205888032913208},
    {'Email': 'nikita.qahud68', 'Response Time': 15.609190940856934},
    {'Email': 'nikita.qahud67', 'Response Time': 15.539058923721313},
    {'Email': 'nikita.qahud70', 'Response Time': 14.10705280303955},  # Изменено время
    {'Email': 'nikita.qahud69', 'Response Time': 13.564427137374878},
    {'Email': 'nikita.qahud71', 'Response Time': 11.121021032333374}
]

# Получение списка email'ов и времени отклика
for i in range(66, 72):
    data.append({'Email': f'nikita.qahud{i}', 'Response Time': 11.7 + (i % 2)})  # чередуем 11 и 12 секунд

# Получение списка времени отклика и количества пользователей
response_times = [entry['Response Time'] for entry in data]
user_numbers = list(range(1, len(data) + 1))  # Порядковые номера пользователей

# Построение графика
plt.figure(figsize=(15, 7))
plt.plot(user_numbers, response_times, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Users Online')
plt.ylabel('Response Time (seconds)')
plt.title('Response Times for Users')

# Настройка оси X для отображения номеров пользователей
plt.xticks(user_numbers)

plt.grid(True)
plt.tight_layout()
plt.savefig('response_times_no_emails.png')
plt.show()
#