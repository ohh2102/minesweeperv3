#!/usr/bin/python
from __future__ import division
import random



class mine:
    def __init__(self):
        self.on_status=False
        self.blown_status=False

class locations:
    def __init__(self, column, row, max_col, max_row):
        self.row=None
        self.column=None
        self.loc_mine=mine()
        self.marked=False
        self.showing=False
        self.adj_cord=[]
        self.adj_col=[]
        self.adj_row=[]
        self.loc_value=0
        self.show_value='*'
        self.save_value=str(self.loc_value)+' ns'
        self.avail=1
        self.adj_col.append(column)
        self.adj_row.append(row)
        if column!=0:
            self.adj_col.append(column-1)
        if column!=max_col-1:
            self.adj_col.append(column+1)
        if row!=0:
            self.adj_row.append(row-1)
        if row!=max_row-1:
            self.adj_row.append(row+1)
        for i in self.adj_col:
            for j in self.adj_row:
                self.adj_cord.append((i,j))
            
        
            
class Game_Board:
    def __init__(self, columns=0, rows=0):
        self.rows=rows
        self.bomb_num=0
        self.columns=columns
        self.total_space=rows*columns
        self.board={}
        self.keys=[]
        for i in range(columns):
            for k in range(rows):
                self.board[(i, k)]=locations(i, k, columns, rows)
                self.keys.append((i,k))
                
    def player_pick(self, row, column):
        if (column,row) in self.board and self.board[(column,row)].showing==False:
            if self.board[(column,row)].loc_mine.on_status==False and self.board[(column,row)].loc_value==0:
                self.board[(column,row)].avail=0.5
                self.board[(column,row)].showing=True
                queue=[]
                queue.append((column, row))
                while len(queue)!=0:
                    search=queue.pop(0)
                    for i in self.board[search].adj_cord:
                        if self.board[i].avail==1 and self.board[i].loc_value==0:
                            self.board[i].avail=0.5
                            self.board[i].showing=True
                            queue.append(i)
                        elif self.board[i].avail==1 and self.board[i].loc_value!=0:
                            self.board[i].showing=True
                            self.board[i].avail=0
                            self.board[i].show_value=self.board[i].loc_value
                            self.board[i].save_value=str(self.board[i].loc_value)+' s'
                        
                    self.board[search].avail=0
                    self.board[search].show_value=self.board[search].loc_value
                    self.board[search].save_value=str(self.board[search].loc_value)+' s'
                    
            elif self.board[(column,row)].loc_mine.on_status==False and self.board[(column,row)].loc_value!=0:
                self.board[(column, row)].show_value=self.board[(column, row)].loc_value
                self.board[(column, row)].avail=0
                self.board[(column, row)].save_value=str(self.board[(column, row)].loc_value)+' s'
                        
                           
                return 1
            else:
                print "YOU LOSE!!"
                return 0
        else:
            print "the coordinates you picked are not on the board"
            return 2
            

            
    def place_bombs(self, numb_bombs):
        bombs_grid=random.sample(self.keys, numb_bombs)
        for bombs_locs in bombs_grid:
            self.board[bombs_locs].loc_mine.on_status=True
            self.board[bombs_locs].save_value=-1
            self.board[bombs_locs].avail=0
            self.board[bombs_locs].save_value='B M'
            for i in self.board[bombs_locs].adj_cord:
                if self.board[i].loc_mine.on_status==False:
                    self.board[i].loc_value=self.board[i].loc_value+1
                    self.board[i].save_value=str(self.board[i].loc_value)+' ns'
            self.bomb_num=numb_bombs
            
    def print_board(self):
        rows_to_print=[]
        current_row=[]
        for i in range(self.rows):
            for j in range(self.columns):
                current_row.append(self.board[(j,i)].show_value)
            rows_to_print.append(current_row)
            current_row=[]
        for k in rows_to_print:
            print '[%s]' % ', '.join(map(str, k))
            
    def any_left(self):
        if all(self.board[values].avail==0 for values in self.board):
            print "YOU WIN"
            return 1
        else:
            return 0
        
    def save_game(self, filename1, filename2):
        f=open(filename1, 'w')
        sorted_dict=sorted(self.board)
        for i in sorted_dict:
            text=self.board[i].save_value
            f.write(text)
            f.write('\n')
        f.close()
        g=open(filename2, 'w')
        g.write(str(self.rows))
        g.write('\n')
        g.write(str(self.columns))
        g.write('\n')
        g.write(str(self.bomb_num))
        g.close()
        
    

def Game():
  
    print "Your Game will start now \n Pick a number of columns and rows each 2 or greater \n if your rows or columns is less than 2 we will use the default size of 10X10"
    try:
        rows=int(raw_input("Enter number rows \n"))
    except:
        print "you made some error entering the number of rows"
        rows=10
    try:
        columns=int(raw_input("Enter number of columns \n"))
    except:
        print "you made some error entering the number of columns"
        columns=10
        
    if rows<2 or columns<2:
        rows=10
        columns=10
    
        
    board_size=rows*columns
    print "Enter the number of mines. It must be less than %d" %board_size
    number_of_mines=int(raw_input())

    Board=Game_Board(columns, rows)
    Board.place_bombs(number_of_mines)
    playing_status=True
    count_moves=0
    
    while playing_status==True:
        
        Board.print_board()
        save_choice=int(raw_input("Enter 0 to save game and 1 to keep playing"))
        if save_choice==1:
            try:
                pick_row=int(raw_input("pick row"))
            except:
                print "ENTER A NUMBER"
                continue
                
            try:
                pick_column=int(raw_input("pick column"))
            except:
                print "ENTER A NUMBER"
                continue
                
            result=Board.player_pick(pick_row,pick_column)
            
            if result==0:
                break
            elif result==1:
                count_moves=count_moves+1
            win_status=Board.any_left()
            if win_status==1:
                break

        else:
            file_name=raw_input("Enter the file to which you want to save the game")
            file_name2=raw_input("Enter second file to which you want to save matrix dimensions")
            Board.save_game(file_name, file_name2)
                        
def Get_or_Play():
    retrieve_or_start=int(raw_input("Enter 1 to start new game. Enter 2 to get a saved 1"))
    if retrieve_or_start==1:
        Game()
    else:
        rows=0
        columns=0
        game_path=raw_input("Enter saved game path")
        game_path2=raw_input("Enter path of matrix dimensions file")
        with open(game_path2, 'r') as g:
            data=[]
            for lines in g:
                data.append(int(lines))
            rows=data[0]
            columns=data[1]
            g.close()
        
        Board=Game_Board(columns, rows)
        with open(game_path, 'r') as f:
            i=0
            k=0
            for lines in f:
                temp_lines=lines.split()
                Board.board[(i,k)].save_value=temp_lines[0]+' '+temp_lines[1]
                k=(k+1)%rows
                if k==0:
                    i=i+1
            f.close()
        for j in Board.board:
            save_values=Board.board[j].save_value.split()
            
            if save_values[1]=='M':
                Board.board[j].loc_mine.on_status=True
                Board.board[j].avail=0
                
            elif save_values[1]=='s':
                Board.board[j].loc_value=int(save_values[0])
                Board.board[j].show_value=int(save_values[0])
                Board.board[j].avail=0
                Board.board[j].showing=True
            elif save_values[1]=='ns':
                Board.board[j].loc_value=int(save_values[0])
   
        playing_status=True
        while playing_status==True:
            Board.print_board()
            save_choice=int(raw_input("Enter 0 to save game and 1 to keep playing"))
            if save_choice==1:
                try:
                    pick_row=int(raw_input("pick row"))
                except:
                    print "ENTER A NUMBER"
                    continue
                    
                try:
                    pick_column=int(raw_input("pick column"))
                except:
                    print "ENTER A NUMBER"
                    continue
                    
                result=Board.player_pick(pick_row,pick_column)
                if result==0:
                    break
                win_status=Board.any_left()
                if win_status==1:
                    break
            else:
                file_name=raw_input("Enter the file to which you want to save the game")
                file_name2=raw_input("Enter second file to which you want to save matrix dimensions")
                Board.save_game(file_name, file_name2)                               
                                 
            
        
        

Get_or_Play()       
        

        
    
        
        

        
     
        
        
        
    
        
        

        



        
        
    
        
        

        
     
        
        
        
    
        
        

        
