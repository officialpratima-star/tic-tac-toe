import javax.swing.*;
import java.awt.*;
import java.util.*;

public class TicToeGUI {
    JButton[][] buttons = new JButton[3][3];
    Random rand = new Random();

    public TicToeGUI() {
        JFrame frame = new JFrame("Tic Tac Toe");
        frame.setLayout(new GridLayout(3,3));
        frame.setSize(300,300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create 3x3 buttons
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                buttons[i][j] = new JButton("");
                int r=i, c=j;
                buttons[i][j].addActionListener(e -> playerMove(r,c));
                frame.add(buttons[i][j]);
            }
        }

        frame.setVisible(true);
    }

    void playerMove(int r,int c){
        if(!buttons[r][c].getText().equals("")) return; // taken
        buttons[r][c].setText("X");
        if(checkWinner("X")) { JOptionPane.showMessageDialog(null,"You win!"); return; }
        computerMove();
    }

    void computerMove(){
        int r,c;
        do{ r=rand.nextInt(3); c=rand.nextInt(3);} while(!buttons[r][c].getText().equals(""));
        buttons[r][c].setText("O");
        if(checkWinner("O")) JOptionPane.showMessageDialog(null,"Computer wins!");
    }

    boolean checkWinner(String s){
        for(int i=0;i<3;i++){
            if(buttons[i][0].getText().equals(s) && buttons[i][1].getText().equals(s) && buttons[i][2].getText().equals(s)) return true;
            if(buttons[0][i].getText().equals(s) && buttons[1][i].getText().equals(s) && buttons[2][i].getText().equals(s)) return true;
        }
        return (buttons[0][0].getText().equals(s) && buttons[1][1].getText().equals(s) && buttons[2][2].getText().equals(s)) ||
               (buttons[0][2].getText().equals(s) && buttons[1][1].getText().equals(s) && buttons[2][0].getText().equals(s));
    }

    public static void main(String[] args) {
        new TicToeGUI();
    }
}



    
    

