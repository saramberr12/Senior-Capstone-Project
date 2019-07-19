package com.example.safercyclinggps;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.Menu;
import android.widget.Button;

import com.example.safercyclinggps.R;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
    public void process(View view) {
        Intent intent = null;

        if (view.getId() == R.id.FastMap) {
            intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("geo:42.3361, 71.0954"));
            Intent chooser = Intent.createChooser(intent, "Launch Maps");
            startActivity(chooser);
        } if (view.getId() == R.id.SafeMap) {
            intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("geo:42.3361, 71.0954"));
            Intent chooser = Intent.createChooser(intent, "Second Maps");
            startActivity(chooser);
        } if (view.getId() == R.id.BestBothMap) {
            intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("geo:42.3361, 71.0954"));
            Intent chooser = Intent.createChooser(intent, "Third Maps");
            startActivity(chooser);
        }
    }
}

