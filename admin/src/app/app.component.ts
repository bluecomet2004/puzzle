import { trigger, transition, style, animate } from '@angular/animations';
import { Component } from '@angular/core';
import { fadeAnimation } from './animations/fadeAnimation';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass'],
  animations: [fadeAnimation]
})
export class AppComponent {
  title = 'admin';
}
