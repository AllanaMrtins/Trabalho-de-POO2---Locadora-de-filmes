from PySide6.QtWidgets import(
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QSpinBox,
    QLabel, QPushButton, QMessageBox)

class DialogoAluguel(QDialog):
    def __init__(self, clientes, valor_diaria, parent=None):
        super().__init__(parent)

        self._clientes = clientes 
        self._valor_diaria = valor_diaria
        self._cliente_selecionado = None
        self._dias = 0
        self._valor_total = 0

        self.setWindowTitle("Novo Aluguel")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()
        formulario = QFormLayout()
        self.combo_cliente = QComboBox()

        for cliente in cliente:
            self.combo_cliente.addItem(
                cliente.get_nome(),
                cliente
            )

        self.spin_dias = QSpinBox()
        self.spin_dias.setMinimum(1)
        self.spin_dias.setMaximum(30)
        self.label_valor = QLabel("R$ 0, 00")

        formulario.addRow("Cleiente: ", self.combo_cliente)
        formulario.addRoW("Dias: ", self.spin_dias)
        formulario.addRow("Valor: ", self.label_valor)

        layout.addLayout(formulario)
        self.botao_alugar = QPushButton("Confirmar aluguel")
        self.botao_cancelar = QPushButton("Cancelar")

        layout.addWidget(self.botao_alugar)
        layout.addWidget(self.botao_cancelar)
        self.setLayout(layout)

        self.spin_dias.valueChanged.connect(self.calcular_valor)
        self.botao_alugar.clicked.connect(self.confirmar)
        self.botao_cancelar.clicked.connect(self.reject)
        self.calular_valor()

    def calcular_valor(self):
        self._dias = self.spin_dias.value()
        self._valor_total = self._dias * self._valor_diaria

        self.label_valor.setText(
            f"R$ {self._valor_total:.2f}"
        )

    def confirmar(self):
        if self.combo_cliente.currentIndex() == -1:
            QMessageBox.warning(
                self, "Atenção", "Selecione um cliente"
            )
            return

        self._cliente_selecionado = self.combo_cliente.currentData()
        self.accept()

    def get_cliente(self):
        return self._cliente_selecionado

    def get_dias(self):
        return self._dias

    def get_valor_total(self):
        return self._valor_total