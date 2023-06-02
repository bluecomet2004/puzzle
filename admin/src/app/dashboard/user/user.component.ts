import { Component, OnInit } from '@angular/core';
import {
  faAngleDoubleLeft,
  faAngleDoubleRight,
  faAngleLeft,
  faAngleRight,
  faEdit,
  faTrash
} from '@fortawesome/free-solid-svg-icons';
import { UserService } from './user.service';
import { UserDashbaord } from './user';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.sass']
})
export class UserComponent implements OnInit {
  firstPageIcon = faAngleDoubleLeft;
  lastPageIcon = faAngleDoubleRight;
  prevPageIcon = faAngleLeft;
  nextPageIcon = faAngleRight;
  editIcon = faEdit;
  deleteIcon = faTrash;

  userData: UserDashbaord = {
    success: true,
    total: 0,
    current_page: 1,
    last_page: 1,
    list: []
  };

  constructor(private userService: UserService) {}
  ngOnInit(): void {
    this.get();
  }

  get(): void {
    this.userService.get().subscribe((response: UserDashbaord): void => {
      this.userData = response;
    });
  }

  formatDateTime(datetime: Date): string {
    const date = new Date(datetime);
    const formattedDate = date.toLocaleDateString('en-US', {year:'numeric',month:'2-digit',day:'2-digit'});
    const formattedTime = date.toLocaleTimeString('en-US', {timeStyle: 'short'});
  
    return `${formattedDate} ${formattedTime}`;
  }
}
