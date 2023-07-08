package developer.servi.capacitybotcleanfinal;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    Button run;
    TextView total, filled, free, test;
    EditText code, crn;
    int total_capacity, filled_capacity, free_capacity;
    String flag = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        run = (Button) findViewById(R.id.run_button);
        code = (EditText) findViewById(R.id.lecture_get);
        crn = (EditText) findViewById(R.id.CRN_get);
        total = (TextView) findViewById(R.id.total_text);
        filled = (TextView) findViewById(R.id.filled_text);
        free = (TextView) findViewById(R.id.free_text);
    }

    public void run_clicked(View v){
        try{
            String lecture_code = code.getText().toString().toUpperCase();
            String searching_crn = crn.getText().toString();
            GetData table = new GetData();
            table.execute(lecture_code, searching_crn);
            while(flag == null){
                Thread.sleep(50);
            }

            total.setText("Total Course Capacity > " + total_capacity);
            filled.setText("Filled Course Capacity > " + filled_capacity);
            if (free_capacity > 0){
                free.setText("Free Capacity > " + free_capacity);
            }
            else{
                free.setText("Course Capacity Is Full!");
            }

        }catch (NumberFormatException | InterruptedException e){
            System.out.println("EXIT > 1");
        }
    }

    class GetData extends AsyncTask<String, String, String>{

        @Override
        protected String doInBackground(String... strings) { //lec_code, crn

            String lec_code = strings[0];
            String crn_string = strings[1];
            ArrayList<String> splitted_list = new ArrayList<String>();
            ArrayList<String> rows_string = new ArrayList<String>();
            int crn_int = Integer.parseInt(crn_string);
            String url = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS&derskodu=" + lec_code;
            try {
                Document page_html = Jsoup.connect(url).timeout(5000).get();
                Elements table = page_html.getElementsByClass("table table-bordered table-striped table-hover table-responsive");
                Elements rows = table.select("tr");
                for(Element row: rows){
                    rows_string.add(row.text());
                }
                int the_row = 0;
                for(String row_string: rows_string){
                    String[] entries = row_string.split(" ");
                    try{
                        int founded_crn = Integer.parseInt(entries[0]);
                        if(founded_crn == crn_int){
                            break;
                        }
                        else{
                            the_row++;
                            continue;
                        }

                    }catch (Exception e){
                        the_row ++;
                        continue;
                    }
                }

                Elements the_entries = rows.get(the_row).select("td");

                for(Element splitted_entries: the_entries){
                    splitted_list.add(splitted_entries.text());
                }

                //splitted_list.get(9) --> total capacity
                //splitted_list.get(10) --> filled capacity
                total_capacity = Integer.parseInt(splitted_list.get(9));
                filled_capacity = Integer.parseInt(splitted_list.get(10));
                free_capacity = total_capacity - filled_capacity;
                flag = "OK";


            } catch (IOException e) {
                System.out.println("EXIT > 2");
            }
            return null;
        }
    }

}

