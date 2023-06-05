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
import { Message, User, UserDashbaord, editUser } from './user';
import Swal from 'sweetalert2';

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

  updateData: editUser = {
    id: "",
    name: ""
  }

  page: number = 1;
  limit: number = 10;
  search: string = '';
  pages: Array<number> = [];
  showEditModal: boolean = false;

  constructor(private userService: UserService) {}
  ngOnInit(): void {
    this.get();
  }

  get(): void {
    this.userService.get(this.page, this.limit, this.search).subscribe((response: UserDashbaord): void => {
      this.userData = response;
      this.pages = [];
      for(let i = 1; i <= this.userData.last_page; i++) {
        this.pages.push(i);
      }
    });
  }

  update(): void {
    this.userService.update(this.updateData.id, this.updateData.name)
      .subscribe((response: Message): void => {
        if(response.success) {
          Swal.fire({
            title: "Success",
            icon: "success",
            text: response.message
          });
        } else {
          Swal.fire({
            title: "Failed",
            icon: "error",
            text: response.message
          });
        }

        this.get();
        this.showEditModal = !this.showEditModal;
      });
  }
  
  delete(id: string): void {
    Swal.fire({
      icon: "question",
      text: "Are you sure you want to delete this user?",
      confirmButtonText: "Yes",
      showCancelButton: true,
      cancelButtonText: "No"
    }).then(result => {
      if(result.isConfirmed) {
        this.userService.delete(id).subscribe((response: Message): void => {
          if(response.success) {
            Swal.fire({
              title: "Success",
              icon: "success",
              text: response.message
            });
          } else {
            Swal.fire({
              title: "Failed",
              icon: "error",
              text: response.message
            });
          }
        });
      }

      this.get();
    });
  }

  formatDateTime(datetime: Date): string {
    const date = new Date(datetime);
    const formattedDate = date.toLocaleDateString('en-US', {year:'numeric',month:'2-digit',day:'2-digit'});
    const formattedTime = date.toLocaleTimeString('en-US', {timeStyle: 'short'});
  
    return `${formattedDate} ${formattedTime}`;
  }

  movePage(page: number): void {
    this.page = page;
    this.get();
  }

  goToNextPage(): void {
    if(this.page < this.userData.last_page) {
      this.page ++;
      this.get();
    }
  }

  goToPrevPage(): void {
    if(this.page > 1) {
      this.page --;
      this.get();
    }
  }

  showModal(user: User): void {
    this.updateData.id = user.id;
    this.updateData.name = user.name;
    this.showEditModal = !this.showEditModal;
  }

  hideModal(event: MouseEvent): void {
    if(event.target === event.currentTarget) {
      this.showEditModal = !this.showEditModal;
    }
  }
}
