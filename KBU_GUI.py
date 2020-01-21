from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import lastKBU as kbu

root = Tk()
root.title('Симуляция работы ВС')
root.geometry('1200x800')

def getValuesAndSimulate():
    output_textField.delete(1.0, END)
    Tzmin = float(Tzmin_Entry.get())
    Tzmax = float(Tzmax_Entry.get())
    Tsmin = float(Tsmin_Entry.get())
    Tsmax = float(Tsmax_Entry.get())
    simTime = int(SimulationTime_Entry.get())
    Texp = int(TobrExp_Entry.get())
    lam = int(LambdaExp_Entry.get())
    value = var.get()
    probability, Q, S, Pc, N_task, T_task, N_buf, T_buf = kbu.simulate(Tzmin, Tzmax, Tsmin, Tsmax, simTime, Texp, lam, value)
    print(sum(probability))

    outPutText = ('P0 = ' + f'{probability[0]}' + '\n' +
                  'P1 = ' + f'{probability[1]}' + '\n' +
                  'P2 = ' + f'{probability[2]}' + '\n' +
                  'P3 = ' + f'{probability[3]}' + '\n' +
                  'P4 = ' + f'{probability[4]}' + '\n' +
                  'Q = ' + f'{Q}' + '\n' +
                  'S = ' + f'{S}' + '\n' +
                  'Pотк = ' + f'{Pc}' + '\n'+
                  'Nпрог = ' + f'{N_task}' + '\n'+
                  'Nбуф = ' + f'{N_buf}' + '\n' +
                  'Tпрог = ' + f'{T_task}' + '\n' +
                  'Tбуф = ' + f'{T_buf}' + '\n')
    output_textField.insert(END, outPutText)

FrameWithBoxes = LabelFrame(root)

SimulationTime_LabelFrame = LabelFrame(FrameWithBoxes)
SimulationTime_label = Label(SimulationTime_LabelFrame, text="Время работы (сек)", font = "Times 14")
SimulationTime_label.pack(side=LEFT, padx=10, pady=10)
SimulationTime_Entry = Entry(SimulationTime_LabelFrame)
SimulationTime_Entry.pack(side=RIGHT, padx=10, pady=10)
SimulationTime_Entry.insert(END, 3600)
SimulationTime_LabelFrame.pack(anchor=W, padx=10, pady=10, fill=X)

LabelTz = LabelFrame(FrameWithBoxes)
Tzmin_label = Label(LabelTz, text="TzMin = ", font = "Times 14")
Tzmin_label.pack(side=LEFT, padx=10, pady=10)
Tzmin_Entry = Entry(LabelTz)
Tzmin_Entry.insert(END, round(1/3, 3))
Tzmin_Entry.pack(side=LEFT, padx=10, pady=10)

Tzmax_label = Label(LabelTz, text="TzMax = ", font = "Times 14")
Tzmax_label.pack(side=LEFT, padx=10, pady=10)
Tzmax_Entry = Entry(LabelTz)
Tzmax_Entry.insert(END, round(2/3, 3))
Tzmax_Entry.pack(side=RIGHT, padx=10, pady=10)
LabelTz.pack(anchor=W, padx=10, pady=10, fill=X)

LabelTs = LabelFrame(FrameWithBoxes)
Tsmin_label = Label(LabelTs, text="TsMin = ", font = "Times 14")
Tsmin_label.pack(side=LEFT, padx=10, pady=10)
Tsmin_Entry = Entry(LabelTs)
Tsmin_Entry.insert(END, 1)
Tsmin_Entry.pack(side=LEFT, padx=10, pady=10)

Tsmax_label = Label(LabelTs, text="TsMax = ", font = "Times 14")
Tsmax_label.pack(side=LEFT, padx=10, pady=10)
Tsmax_Entry = Entry(LabelTs)
Tsmax_Entry.pack(side=RIGHT, padx=10, pady=10)
Tsmax_Entry.insert(END, 6)
LabelTs.pack(anchor=W, padx=10, pady=10, fill=X)

LabelExp = LabelFrame(FrameWithBoxes)
LambdaExp_label = Label(LabelExp, text = 'λ = ', font = "Times 14")
LambdaExp_label.pack(side=LEFT, padx=10, pady=10)
LambdaExp_Entry = Entry(LabelExp)
LambdaExp_Entry.insert(END, 2)
LambdaExp_Entry.pack(side=LEFT, padx=10, pady=10)

TobrExp_label = Label(LabelExp, text = 'Tобр = ', font = "Times 14")
TobrExp_label.pack(side=LEFT, padx=10, pady=10)
TobrExp_Entry = Entry(LabelExp)
TobrExp_Entry.insert(END, 3)
TobrExp_Entry.pack(side=RIGHT, padx=10, pady=10)
LabelExp.pack(anchor=W, padx=10, pady=10, fill=X)

VarLabel = LabelFrame(FrameWithBoxes)
var = IntVar()
var.set(1)
LinearR = Radiobutton(VarLabel, text = 'Линейная', variable = var, value = 1, font = "Times 14")
ExpR = Radiobutton(VarLabel, text = 'Экспоненциальная', variable = var, value = 2, font = "Times 14")
LinearR.pack()
ExpR.pack()
VarLabel.pack(anchor = W, padx = 10, pady = 10, fill = X)

DescriptionLabel = Label(FrameWithBoxes, text = '''- P0 – вероятность того, что ВС не загружена,
- P1 – вероятность того, что сервер обрабатывает одну программу и буфер пуст,
- P2 – вероятность того, что в буфере находится 1-на программа,
- P3 – вероятность того, что в буфере находится 2-ве программы,
- P4 – вероятность того, что в буфере находится 3-ри программы,
- Q – относительная пропускная способность ВС – средняя доля программ,
обработанных ВС,
- S – абсолютная пропускная способность – среднее число программ, 
обработанныхв единицу времени,
- P отк – вероятность отказа, т.е. того, что программа будет не обработанной,
- N прог – среднее число программ в ВС,
- T прог – среднее время нахождения программы в ВС,
- N буф – среднее число программ в буфере,
- T буф – среднее время нахождения программы в буфере. ''', font = "Times 10")
DescriptionLabel.pack(fill = BOTH, pady = 50)

FrameWithOutput = LabelFrame(root)

output_textField = Text(FrameWithOutput, height=40)
output_textField.pack(padx=10, pady=10, side=TOP)

FrameWithOutput.pack(side=RIGHT, padx=5, pady=10, fill=Y)


Work = Button(FrameWithBoxes, text = "За работу!", command = getValuesAndSimulate)
Work.pack(side = BOTTOM, padx = 5, pady = 10)

FrameWithBoxes.pack(side=LEFT, padx=5, pady=10, fill=Y)




root = mainloop()