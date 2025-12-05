#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CalculadoraJuros:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Juros Diários")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Variáveis de controle
        self.var_valor = tk.StringVar()
        self.var_data_vencimento = tk.StringVar()
        
        # Referências para atualização dos cards
        self.lbl_dias = None
        self.lbl_juros = None
        self.lbl_total = None
        self.lbl_status = None
        
        self.criar_interface()
        
    def criar_interface(self):
        # --- Frame Principal ---
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # --- Cabeçalho (Estilo visual do seu exemplo) ---
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False) # Mantém altura fixa
        
        title = tk.Label(
            header_frame,
            text="💰 CÁLCULO DE JUROS SIMPLES E MULTAS",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=(25, 5))
        
        subtitle = tk.Label(
            header_frame,
            text="Taxa aplicada: 2,5% ao dia",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        subtitle.pack()

        # --- Área de Inputs (Entrada de Dados) ---
        input_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        input_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)
        
        # Grid para inputs
        tk.Label(input_frame, text="Valor do Boleto (R$):", font=('Arial', 11), bg='white').grid(row=0, column=0, padx=20, pady=(20, 5), sticky='w')
        entry_valor = tk.Entry(input_frame, textvariable=self.var_valor, font=('Arial', 12), width=20)
        entry_valor.grid(row=1, column=0, padx=20, pady=(0, 20), sticky='w')
        
        tk.Label(input_frame, text="Data de Vencimento (dd/mm/aaaa):", font=('Arial', 11), bg='white').grid(row=0, column=1, padx=20, pady=(20, 5), sticky='w')
        entry_data = tk.Entry(input_frame, textvariable=self.var_data_vencimento, font=('Arial', 12), width=20)
        entry_data.grid(row=1, column=1, padx=20, pady=(0, 20), sticky='w')
        
        # Botão Calcular
        btn_calcular = tk.Button(
            input_frame,
            text="✅ Calcular Juros",
            command=self.calcular,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        btn_calcular.grid(row=1, column=2, padx=20, pady=(0, 20), sticky='w')

        # --- Área de Resultados (Cards) ---
        cards_frame = tk.Frame(main_frame, bg='#f0f0f0')
        cards_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Configuração das colunas do grid
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        cards_frame.columnconfigure(3, weight=1)

        # Criação dos Cards (Inicialmente zerados)
        self.lbl_status = self.criar_card(cards_frame, "Status", "Aguardando", "#7f8c8d", 0)
        self.lbl_dias = self.criar_card(cards_frame, "Dias de Atraso", "0", "#e67e22", 1)
        self.lbl_juros = self.criar_card(cards_frame, "Valor dos Juros", "R$ 0,00", "#c0392b", 2)
        self.lbl_total = self.criar_card(cards_frame, "Total Atualizado", "R$ 0,00", "#2980b9", 3)

        # --- Rodapé ---
        footer_frame = tk.Frame(main_frame, bg='#f0f0f0')
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_limpar = tk.Button(
            footer_frame,
            text="🧹 Limpar Campos",
            command=self.limpar,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15
        )
        btn_limpar.pack(side=tk.LEFT)
        
        tk.Label(footer_frame, text=f"Data de hoje: {datetime.now().strftime('%d/%m/%Y')}", bg='#f0f0f0', fg='#7f8c8d').pack(side=tk.RIGHT)

    def criar_card(self, parent, titulo, valor_inicial, cor, coluna):
        """Cria um card estilizado igual ao código de referência."""
        card = tk.Frame(parent, bg=cor, relief=tk.RAISED, borderwidth=2)
        card.grid(row=0, column=coluna, padx=5, pady=5, sticky='ew')
        
        tk.Label(
            card,
            text=titulo,
            font=('Arial', 10, 'bold'),
            bg=cor,
            fg='white'
        ).pack(pady=(15, 5))
        
        lbl_valor = tk.Label(
            card,
            text=valor_inicial,
            font=('Arial', 14, 'bold'),
            bg=cor,
            fg='white'
        )
        lbl_valor.pack(pady=(0, 15))
        
        return lbl_valor

    def calcular(self):
        """Realiza o cálculo dos juros."""
        valor_str = self.var_valor.get().replace(',', '.')
        data_str = self.var_data_vencimento.get()
        
        # Validação básica
        if not valor_str or not data_str:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            # 1. Converter valores
            valor_original = float(valor_str)
            data_vencimento = datetime.strptime(data_str, '%d/%m/%Y')
            data_hoje = datetime.now()
            
            # 2. Calcular dias de atraso
            diferenca = data_hoje - data_vencimento
            dias_atraso = diferenca.days
            
            # 3. Lógica de Juros
            taxa_diaria = 0.025 # 2.5%
            
            if dias_atraso > 0:
                valor_juros = valor_original * taxa_diaria * dias_atraso
                valor_total = valor_original + valor_juros
                
                # Atualizar Interface - Caso Atrasado
                self.atualizar_card(self.lbl_status, "ATRASADO", "Vencido")
                self.atualizar_card(self.lbl_dias, f"{dias_atraso} dias", "Dias")
                self.atualizar_card(self.lbl_juros, f"R$ {valor_juros:,.2f}", "Juros")
                self.atualizar_card(self.lbl_total, f"R$ {valor_total:,.2f}", "Total")
            
            else:
                # Caso não esteja vencido
                self.atualizar_card(self.lbl_status, "EM DIA", "Ok")
                self.atualizar_card(self.lbl_dias, "0", "Dias")
                self.atualizar_card(self.lbl_juros, "R$ 0,00", "Juros")
                self.atualizar_card(self.lbl_total, f"R$ {valor_original:,.2f}", "Total")
                
                if dias_atraso < 0:
                    msg = f"Este boleto vencerá em {abs(dias_atraso)} dias."
                else:
                    msg = "O boleto vence hoje."
                messagebox.showinfo("Informação", msg)

        except ValueError:
            messagebox.showerror("Erro", "Formato inválido!\n\nUse ponto para decimais (ex: 1000.50)\nUse datas no formato DD/MM/AAAA")

    def atualizar_card(self, label, texto, tipo):
        """Atualiza o texto de um card."""
        label.config(text=texto)
        
    def limpar(self):
        """Limpa os campos e reseta os cards."""
        self.var_valor.set("")
        self.var_data_vencimento.set("")
        self.lbl_status.config(text="Aguardando")
        self.lbl_dias.config(text="0")
        self.lbl_juros.config(text="R$ 0,00")
        self.lbl_total.config(text="R$ 0,00")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraJuros(root)
    root.mainloop()