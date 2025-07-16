export interface Practitioner {
  id: number;
  name: string;
  specialty: string;
  rating: number;
  experience: string;
  location: string;
  nextAvailable: string;
  image: string;
}

export interface PractitionerResponse {
  practitioners: Practitioner[];
  total: number;
}

export interface ApiError {
  message: string;
  status: number;
}