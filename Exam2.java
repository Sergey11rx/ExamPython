// Напишите проект для розыгрыша в магазине игрушек. Функционал должен содержать добавление 
// новых игрушек и задания веса для выпадения игрушек.



import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

class Toy {
    private int id;
    private String name;
    private int quantity;
    private double weight;

    public Toy(int id, String name, int quantity, double weight) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.weight = weight;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getQuantity() {
        return quantity;
    }

    public double getWeight() {
        return weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }
}

class ToyStore {
    private List<Toy> toys;
    private List<Toy> prizeToys;

    public ToyStore() {
        toys = new ArrayList<>();
        prizeToys = new ArrayList<>();
    }

    public void addToy(Toy toy) {
        toys.add(toy);
    }

    public void updateToyWeight(int toyId, double weight) {
        for (Toy toy : toys) {
            if (toy.getId() == toyId) {
                toy.setWeight(weight);
                break;
            }
        }
    }

    public Toy selectPrizeToy() {
        double totalWeight = toys.stream().mapToDouble(Toy::getWeight).sum();
        double random = new Random().nextDouble() * totalWeight;

        double cumulativeWeight = 0;
        for (Toy toy : toys) {
            cumulativeWeight += toy.getWeight();
            if (random < cumulativeWeight) {
                toys.remove(toy);
                prizeToys.add(toy);
                return toy;
            }
        }

        return null;  // Игрушек в наличии нет
    }

    public void savePrizeToyToFile(String filePath, Toy toy) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            writer.write(toy.getName());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void decreaseToyQuantity(int toyId) {
        for (Toy toy : toys) {
            if (toy.getId() == toyId) {
                toy.quantity--;
                break;
            }
        }
    }
}

public class ToyGameApp {
    public static void main(String[] args) {
        ToyStore toyStore = new ToyStore();

        // Добавление игрушек
        toyStore.addToy(new Toy(1, "Car", 10, 20));
        toyStore.addToy(new Toy(2, "Doll", 8, 30));
        toyStore.addToy(new Toy(3, "Ball", 15, 15));

        // Обновление веса игрушки
        toyStore.updateToyWeight(2, 40);

        // Выбор призовой игрушки
        Toy prizeToy = toyStore.selectPrizeToy();
        if (prizeToy != null) {
            // Сохранение призовой игрушки в файл
            toyStore.savePrizeToyToFile("prize_toy.txt", prizeToy);

            // Уменьшение количества игрушек
            toyStore.decreaseToyQuantity(prizeToy.getId());
        }
    }
}
