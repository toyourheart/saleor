import * as React from "react";
import MuiTable, {
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow
} from "material-ui/Table";
import Typography from "material-ui/Typography";
import { withStyles } from "material-ui/styles";
import { TablePagination } from "./TablePagination";

interface PageInfo {
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

interface TableProps {
  headers: Array<{
    label: string;
    name: string;
    wide?: boolean;
  }>;
  onNextPage(event);
  onPreviousPage(event);
  page: PageInfo;
}

export const Table: React.StatelessComponent<TableProps> = ({
  children,
  headers,
  onNextPage,
  onPreviousPage,
  page
}) => (
  <MuiTable>
    <TableHead>
      <TableRow>
        {headers.map(header => (
          <TableCell key={header.name}>{header.label}</TableCell>
        ))}
      </TableRow>
    </TableHead>
    <TableBody>{children}</TableBody>
    <TableFooter>
      <TableRow>
        <TablePagination
          colSpan={5}
          hasNextPage={page.hasNextPage}
          hasPreviousPage={page.hasPreviousPage}
          onNextPage={onNextPage}
          onPreviousPage={onPreviousPage}
        />
      </TableRow>
    </TableFooter>
  </MuiTable>
);

export default Table;